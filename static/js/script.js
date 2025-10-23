document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('lotteryForm');
    const gameSelect = document.getElementById('game_type');
    
    form.addEventListener('submit', function(event) {
        if (!gameSelect.value) {
            alert('❌ Por favor, selecione um jogo!');
            event.preventDefault();
            return;
        }
        const fileInput = document.getElementById('file');
        if (!fileInput.files.length) {
            alert('❌ Por favor, selecione um arquivo Excel!');
            event.preventDefault();
        }
    });
    
    // Auto-focus no select
    gameSelect.focus();
});