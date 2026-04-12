from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    from app.models import User, Expense

    from app.routes.user_authorization import auth_bp
    from app.routes.expenses import expenses_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(expenses_bp, url_prefix="/api/expenses")

    from app.exceptions.handlers import register_error_handlers
    register_error_handlers(app)

    return app