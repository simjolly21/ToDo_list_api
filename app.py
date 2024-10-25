# app.py
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Import and register blueprints
from resources.auth import auth_bp
from resources.todos import todos_bp

app.register_blueprint(auth_bp)
app.register_blueprint(todos_bp)

if __name__ == '__main__':
    app.run(debug=True)
