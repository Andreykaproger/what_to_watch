from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)

from . import cli_commands, error_handlers, views, api_views, decorators
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))