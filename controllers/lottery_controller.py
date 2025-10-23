from flask import Blueprint, render_template, request, flash
from models.lottery_model import LotteryModel

lottery_bp = Blueprint('lottery', __name__)

@lottery_bp.route('/', methods=['GET', 'POST'])
def index():
    games = list(LotteryModel.GAME_CONFIG.keys())
    suggestions = None
    selected_game = None
    
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
                suggestions = [[int(num) for num in LotteryModel.generate_game(probs, total, pick)] for _ in range(5)]
                selected_game = game_type
            except Exception as e:
                flash(f"Erro: {str(e)}")
        else:
            flash("Por favor, selecione um jogo e faça upload do arquivo.")
    
    return render_template('index.html', games=games, suggestions=suggestions, selected_game=selected_game)