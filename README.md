## 📁 COMO USAR

# 🎰 Lottery Suggestion Portal - Loterias CAIXA

Este repositório fornece um portal simples em Flask para analisar históricos de sorteios (planilhas Excel) e gerar sugestões de jogos para diversas loterias da CAIXA. Recentemente foi adicionada uma integração opcional com um modelo generativo (Gemini) para enriquecer as sugestões com estimativas de chance.

## 🚀 SETUP RÁPIDO

1. Clone ou extraia o projeto
2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
# Mac/Linux
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute o projeto:

```bash
python app.py
```

5. Acesse no navegador:

```
http://127.0.0.1:5000
```

---

## 📊 JOGOS SUPORTADOS (configuração atual)

- Lotofácil — 15/25
- Quina — 5/80
- Mega-Sena — 6/60
- Lotomania — 50/100
- Dupla Sena — 6/50
- Timemania — 10/80
- Dia de Sorte — 7/31
- Super Sete — 7/10
- Federal / Loteca — formatos especiais

Consulte `models/lottery_model.py` para ver a configuração completa e como as colunas da planilha são lidas.

---

## ✨ Integração com IA (opcional)

Adicionamos suporte para enviar um prompt ao endpoint da Google Generative Language (Gemini) para gerar até 5 sugestões com uma estimativa de chance para cada jogo. A integração é opcional: se a variável de ambiente não estiver definida ou a chamada falhar, o portal continuará funcionando com a lógica local de frequências.

- Variável de ambiente:

```bash
export GOOGLE_GEN_API_KEY="SUA_CHAVE_AQUI"
```

- Endpoint usado (exemplo):

```
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=API_KEY
```

- Payload mínimo enviado (JSON):

```json
{
   "contents": [
      { "parts": [ { "text": "<PROMPT COM O HISTÓRICO>" } ] }
   ]
}
```

Observações importantes sobre o comportamento da IA:

- O serviço espera receber um JSON válido da IA com o formato abaixo (o prompt pede explicitamente para retornar apenas esse JSON):

```json
{
   "suggestions": [
      { "numbers": [1,2,3,...], "chance": 30.0, "reason": "breve explicação" },
      ... (até 5)
   ]
}
```

- A implementação tenta extrair um JSON mesmo quando o modelo retorna texto extra (usa heurísticas para localizar JSON embutido). Se tiver exemplos reais de retorno da API (sem a chave), cole aqui e eu adapto o parser para o formato exato.

---

## Como as sugestões são exibidas

- A interface gera 5 sugestões de jogo. Quando a IA responde corretamente, o portal prioriza as 5 sugestões da IA (com `chance` e `reason` mostrados). Se a IA retornar menos de 5 sugestões, o sistema completa com sugestões locais geradas a partir da análise de frequência.
- Cada sugestão exibida na UI tem estes campos:
   - números (lista)
   - chance (porcentagem; fornecida pela IA ou calculada como fallback a partir de scores locais)
   - reason (frase curta quando disponível)
   - source (IA ou LOCAL)

Exemplo de exibição desejada:

```
🎲 1 Sugestão 30%
1, 3, 5, 6, 7, 9, 10, 14, 15, 16, 17, 18, 19, 20, 22

🎲 2 Sugestão 25%
1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 16, 18, 20, 22, 24
```

---

## Arquivos principais modificados / novos

- `controllers/ia_service.py` — novo: serviço que monta o prompt, chama a API Gemini e normaliza a resposta JSON (tenta extrair `numbers`, `chance`, `reason`).
- `controllers/lottery_controller.py` — agora prioriza sugestões da IA, completa com sugestões locais quando necessário e prepara o objeto `suggestions` para o template.
- `models/lottery_model.py` — lógica de leitura da planilha, cálculo de frequências e geração local de jogos (sem alterações estruturais críticas, mas usado como fallback).
- `templates/index.html` — UI atualizada para exibir `numbers`, `chance`, `reason` e `source` para cada sugestão.
- `requirements.txt` — adicionado `requests` para chamadas HTTP.

---

## Comportamento de fallback e robustez

- Se `GOOGLE_GEN_API_KEY` não estiver definida ou a chamada falhar, o portal gera 5 sugestões locais usando uma amostragem ponderada pelas frequências calculadas.
- Para sugestões locais que completam a lista (quando a IA não retorna 5), o sistema calcula um score simples (soma das probabilidades individuais dos números) e normaliza esses scores para produzir porcentagens de fallback.

---

## Depuração e logs

- Se quiser inspecionar o texto cru retornado pela API (útil para ajustar o parser), podemos adicionar logging temporário em `controllers/ia_service.py` para salvar a resposta em um arquivo ou imprimir no console.

---

## Testes rápidos e validação

1. Configure a chave (opcional) e rode a aplicação
2. Faça upload de uma planilha Excel com as colunas de bolas conforme esperado (veja `GAME_CONFIG` em `models/lottery_model.py`)
3. Verifique a seção de sugestões; se a IA estiver disponível e obedecer ao esquema JSON, você verá as porcentagens vindas da IA. Caso contrário, verá porcentagens calculadas localmente.

---

## Próximos passos sugeridos

- Forçar no prompt que as porcentagens somem 100% (se desejar uma distribuição fechada).  
- Implementar cache simples (memória) para respostas da IA por hash do histórico, reduzindo custos e latência.  
- Adicionar testes unitários para parsing de respostas da IA e geração local de sugestões.

Se quiser que eu aplique qualquer um desses próximos passos (por exemplo: cache, ajuste do prompt para somar 100%, ou logs do texto cru retornado), diga qual e eu implemento.

---

## 🔧 COMANDOS ÚTEIS

```bash
# Parar servidor
Ctrl + C

# Desativar ambiente virtual
deactivate

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```


## 🤖 Integração com IA (opcional)

Este projeto pode usar um modelo generativo (ex.: Gemini) para enriquecer as sugestões com estimativas de chance.

- Configure a variável de ambiente `GOOGLE_GEN_API_KEY` com sua chave de API (NUNCA commit a chave no repositório):

```bash
export GOOGLE_GEN_API_KEY="sua_chave_aqui"
```

- Em seguida, rode a aplicação normalmente. Se a variável estiver configurada, a aplicação enviará os últimos sorteios para a API e exibirá sugestões da IA com porcentagens.

Observação: a integração depende do endpoint da Google Generative Language e do formato de resposta. Caso a API retorne texto que não seja JSON, o serviço tentará parsear padrões simples — por isso, recomenda-se revisar o prompt/retorno para garantir compatibilidade.