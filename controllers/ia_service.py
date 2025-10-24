import os
import json
import re
import requests
from typing import List, Dict, Optional


API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'


def _extract_text_from_response(resp_json: dict) -> Optional[str]:
    # Try common structured fields
    for key in ('candidates', 'output', 'responses'):
        block = resp_json.get(key)
        if isinstance(block, list) and len(block) > 0:
            first = block[0]
            if isinstance(first, dict):
                # procurar por content -> list -> text
                content = first.get('content') or first.get('message') or first.get('output')
                if isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
                    # procurar por 'text'
                    for part in content:
                        if isinstance(part, dict) and 'text' in part:
                            return part['text']
                # direto
                if 'text' in first and isinstance(first['text'], str):
                    return first['text']

    # fallback: se json tiver 'text' em qualquer lugar
    def find_text(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k == 'text' and isinstance(v, str):
                    return v
                res = find_text(v)
                if res:
                    return res
        if isinstance(d, list):
            for it in d:
                res = find_text(it)
                if res:
                    return res
        return None

    return find_text(resp_json)


def _extract_json_from_text(text: str) -> Optional[dict]:
    """Tenta extrair e parsear o primeiro JSON válido dentro de uma string de texto qualquer."""
    if not text or not isinstance(text, str):
        return None

    # procura por substring que comece com { ou [ e termine com } ou ]
    # estratégia simples: encontre primeiro '{' ou '[' e última ocorrência correspondente e tente carregar
    starts = [m.start() for m in re.finditer(r'[\{\[]', text)]
    ends = [m.start() for m in re.finditer(r'[\}\]]', text)]
    if not starts or not ends:
        return None

    for s in starts:
        # tentar cada end >= s
        for e in reversed(ends):
            if e <= s:
                continue
            candidate = text[s:e+1]
            try:
                return json.loads(candidate)
            except Exception:
                continue

    # última tentativa: parsear inteiro
    try:
        return json.loads(text)
    except Exception:
        return None


def analyze_with_gemini(draws: List[List[int]], game_type: str, total: int, pick: int, num_recent: int = 100) -> Optional[List[Dict]]:
    """
    Envia um prompt para a API Gemini pedindo 5 sugestões e uma estimativa de chance para cada uma.
    Retorna uma lista de objetos: {'numbers': [..], 'chance': 12.3, 'reason': '...'}
    Em caso de erro ou ausência de chave, retorna None.
    """
    api_key = os.environ.get('GOOGLE_GEN_API_KEY')
    if not api_key:
        return None

    recent = draws[-num_recent:]
    recent_text = '\n'.join([', '.join(map(str, d)) for d in recent])

    prompt = (
        f"Você é um assistente especializado em análise estatística de loterias. Recebe um histórico de sorteios e deve retornar EXACTAMENTE um JSON válido com a seguinte estrutura:\n"
        "{\n  \"suggestions\": [\n    { \"numbers\": [int], \"chance\": float, \"reason\": string },\n    ...\n  ]\n}\n"
        "Gere 5 (cinco) sugestões para o jogo solicitado, cada sugestão deve ter exatamente o número de bolas esperadas. 'chance' é uma porcentagem (por exemplo 12.5). 'reason' é uma frase curta explicando a escolha. NÃO inclua texto antes ou depois do JSON.\n\n"
        f"Jogo: {game_type}\nTotal números: {total}, pick: {pick}\nÚltimos {len(recent)} sorteios (cada linha um sorteio):\n{recent_text}\n\n"
        "Retorne somente o JSON acima."
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(f"{API_URL}?key={api_key}", json=payload, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        # Extrair texto que contenha o JSON
        text = _extract_text_from_response(data)
        if not text:
            text = json.dumps(data)

        parsed = _extract_json_from_text(text)
        if not parsed:
            return None

        suggestions = parsed.get('suggestions')
        if not isinstance(suggestions, list):
            return None

        out = []
        for s in suggestions[:5]:
            nums = s.get('numbers') if isinstance(s.get('numbers'), list) else []
            nums = [int(n) for n in nums][:pick]
            chance = float(s.get('chance')) if s.get('chance') not in (None, '') else 0.0
            reason = s.get('reason') if isinstance(s.get('reason'), str) else ''
            out.append({'numbers': nums, 'chance': round(chance, 2), 'reason': reason})

        return out if out else None
    except Exception:
        return None

