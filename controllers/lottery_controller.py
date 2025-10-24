from flask import Blueprint, render_template, request, flash
from models.lottery_model import LotteryModel
from controllers.ia_service import analyze_with_gemini

lottery_bp = Blueprint('lottery', __name__)


@lottery_bp.route('/', methods=['GET', 'POST'])
def index():
    games = list(LotteryModel.GAME_CONFIG.keys())
    suggestions = None
    selected_game = None
    final_suggestions = None

    if request.method == 'POST':
        game_type = request.form.get('game_type')
        num_recent = int(request.form.get('num_recent', 100))
        file = request.files.get('file')

        if file and game_type:
            try:
                draws, total, pick = LotteryModel.parse_data(file, game_type)
                if not draws:
                    flash("Nenhum sorteio válido encontrado no arquivo.")
                    return render_template('index.html', games=games)

                probs = LotteryModel.analyze_frequencies(draws, total, num_recent)
                # sugestões locais (baseadas em probabilidades locais)
                local_suggestions = [[int(num) for num in LotteryModel.generate_game(probs, total, pick)] for _ in range(5)]
                selected_game = game_type

                # Tenta obter sugestões da IA
                ia_sugs = None
                try:
                    ia_sugs = analyze_with_gemini(draws, game_type, total, pick, num_recent)
                except Exception:
                    ia_sugs = None

                final = []
                if ia_sugs:
                    # usar sugestões da IA como prioridade
                    for item in ia_sugs:
                        nums = item.get('numbers', [])
                        chance = item.get('chance')
                        reason = item.get('reason', '')
                        final.append({'numbers': nums, 'chance': chance, 'reason': reason, 'source': 'ia'})

                # Se IA retornou menos de 5, completar com sugestões locais
                if len(final) < 5:
                    # calcular score simples para cada sugestão local (soma das probs)
                    scores = []
                    for nums in local_suggestions:
                        s = sum([probs[n-1] for n in nums]) if probs is not None else 0
                        scores.append(max(s, 0.0))
                    total_score = sum(scores) or 1.0
                    # transformar em porcentagens apenas para as 5 locais
                    local_percentages = [round((sc / total_score) * 100, 2) for sc in scores]

                    # adicionar apenas o necessário para completar 5
                    need = 5 - len(final)
                    for i in range(need):
                        nums = local_suggestions[i]
                        chance = local_percentages[i]
                        final.append({'numbers': nums, 'chance': chance, 'reason': '', 'source': 'local'})

                # garantir exatamente 5
                final_suggestions = final[:5]

            except Exception as e:
                flash(f"Erro: {str(e)}")
        else:
            flash("Por favor, selecione um jogo e faça upload do arquivo.")

    return render_template('index.html', games=games, suggestions=final_suggestions, selected_game=selected_game)