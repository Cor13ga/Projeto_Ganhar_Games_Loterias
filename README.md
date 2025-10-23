# 🎰 Lottery Suggestion Portal - Loterias CAIXA

## 🚀 SETUP RÁPIDO

1. **Clone ou extraia o projeto**
2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
````

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o projeto:**

   ```bash
   python app.py
   ```

5. **Acesse no navegador:**

   ```
   http://127.0.0.1:5000
   ```

---

## 📊 JOGOS SUPORTADOS

| Jogo         | Números | Intervalo |
| ------------ | ------- | --------- |
| Lotofácil    | 15/25   | 1–25      |
| Quina        | 5/80    | 1–80      |
| Mega-Sena    | 6/60    | 1–60      |
| Lotomania    | 50/100  | 0–99      |
| Dupla Sena   | 6/50    | 1–50      |
| Timemania    | 10/80   | 1–80      |
| Dia de Sorte | 7/31    | 1–31      |
| Super Sete   | 7/10    | 0–9       |

---


## ESTRUTURA DA PASTA

lottery-portal/
├── .venv/
├── app.py                  
├── requirements.txt        
├── README.md               
├── models/
│   └── lottery_model.py    
├── controllers/
│   └── lottery_controller.py  
├── templates/
│   └── index.html          
└── static/
    ├── css/
    │   └── style.css       
    └── js/
        └── script.js      

## 📁 COMO USAR

1. Baixe o **histórico da loteria** em formato `.xlsx`
2. Selecione o tipo de jogo no portal
3. Faça o **upload** do arquivo Excel
4. Receba **5 sugestões** baseadas na análise estatística

---

## ✅ TESTE RÁPIDO

1. Use sua planilha `Lotofácil.xlsx`
2. Selecione o jogo **Lotofácil**
3. Faça o upload do arquivo
4. Clique em **"Gerar 5 Sugestões"**

🎉 **Pronto!** O portal está funcionando!

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