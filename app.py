from flask import Flask
from controllers.lottery_controller import lottery_bp

app = Flask(__name__, static_folder='static')
app.register_blueprint(lottery_bp)

if __name__ == '__main__':
    app.run(debug=True)