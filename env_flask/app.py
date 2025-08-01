from flask import Flask
from flask_jwt_extended import JWTManager
from database import init_db
from routes import bp as api_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Troque em produção
app.config['JSON_SORT_KEYS'] = False

jwt = JWTManager(app)

init_db()

app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)
