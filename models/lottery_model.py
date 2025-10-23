import pandas as pd
import numpy as np
from io import BytesIO

class LotteryModel:
    GAME_CONFIG = {
        'Lotofácil': {'total': 25, 'pick': 15, 'bola_cols': [f'Bola{i}' for i in range(1, 16)]},
        'Quina': {'total': 80, 'pick': 5, 'bola_cols': [f'Bola{i}' for i in range(1, 6)]},
        'Mega-Sena': {'total': 60, 'pick': 6, 'bola_cols': [f'Bola{i}' for i in range(1, 7)]},
        'Lotomania': {'total': 100, 'pick': 50, 'bola_cols': [f'Bola{i}' for i in range(1, 51)]},
        'Dupla Sena': {'total': 50, 'pick': 6, 'bola_cols': [f'Bola{i}' for i in range(1, 7)]},
        'Timemania': {'total': 80, 'pick': 10, 'bola_cols': [f'Bola{i}' for i in range(1, 11)]},
        'Dia de Sorte': {'total': 31, 'pick': 7, 'bola_cols': [f'Bola{i}' for i in range(1, 8)]},
        'Super Sete': {'total': 10, 'pick': 7, 'bola_cols': [f'Bola{i}' for i in range(1, 8)]},
        'Federal': {'total': 6, 'pick': 6, 'bola_cols': [f'Bola{i}' for i in range(1, 7)]}, 
        'Loteca': {'total': 14, 'pick': 14, 'bola_cols': [f'Bola{i}' for i in range(1, 15)]}  
    }

    @staticmethod
    def parse_data(file, game_type):
        if game_type not in LotteryModel.GAME_CONFIG:
            raise ValueError("Unsupported game type")
        
        config = LotteryModel.GAME_CONFIG[game_type]
        df = pd.read_excel(file)
        draws = []
        for _, row in df.iterrows():
            numbers = sorted([int(row[col]) for col in config['bola_cols'] if col in df.columns and not pd.isna(row[col])])
            if len(numbers) == config['pick']:
                draws.append(numbers)
        return draws, config['total'], config['pick']

    @staticmethod
    def analyze_frequencies(draws, total_numbers, num_recent=100):
        recent_draws = draws[-num_recent:]
        freq = np.zeros(total_numbers + 1)
        for draw in recent_draws:
            for num in draw:
                freq[num] += 1
        total_occ = sum(freq)
        probs = np.ones(total_numbers + 1) / total_numbers if total_occ == 0 else freq / total_occ
        probs[0] = 0
        probs /= probs.sum()
        return probs[1:]

    @staticmethod
    def generate_game(probs, total_numbers, pick_numbers):
        numbers = np.arange(1, total_numbers + 1)
        selected = np.random.choice(numbers, size=pick_numbers, replace=False, p=probs)
        return sorted(selected)