from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
import os
import secrets
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from itsdangerous import URLSafeSerializer as Serializer
from flask_mail import Mail

UPLOAD_IMG = ''
bcrypt =  Bcrypt()
db = SQLAlchemy()
mail = Mail()
app = ''
def Create_app():
    global app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secrets.token_hex(17)
    # app.config['SECRET_KEY'] = "orenoimoutogakonanikawaiwakejanaii"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)),'database.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    global UPLOAD_IMG
    UPLOAD_IMG = os.path.join(app.root_path, './static/img') 
    app.config['UPLOAD_FOLDER'] = 'UPLOAD_IMG'
    
    
    bcrypt.init_app(app)
    db.init_app(app)
    
    from .auth import auth
    from .views import views
    from .Errors.handlers import errors
    
    app.register_blueprint(auth)
    app.register_blueprint(views)
    app.register_blueprint(errors)
    
    
    from .models import User,Post
    create_db(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
        
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    mail.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    return app


def create_db(app):
    with app.app_context():
        db.create_all()
