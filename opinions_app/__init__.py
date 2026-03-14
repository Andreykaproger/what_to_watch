from apiflask import APIFlask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from settings import Config


app = APIFlask(
    __name__,
    title="What to Watch API",
    version="1.0",
    docs_path="/api/docs"
)
app.config.from_object(Config)
db = SQLAlchemy(app)
jwt = JWTManager()
jwt.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'access.login_view'

migrate = Migrate(app, db)

from . import error_handlers
from .utils import decorators, cli_commands
from .models import User, TokenBlockList

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):

    jti = jwt_payload['jti']

    token = TokenBlockList.query.filter_by(
        jti = jti
    ).first()

    return token is not None

from opinions_app.users import users_bp
from opinions_app.opinions import opinions_bp
from opinions_app.admin import admin_bp
from opinions_app.access_managment import access_bp
from opinions_app.api import opinions_api_bp, auth_api_bp, admin_api_bp

app.register_blueprint(users_bp)
app.register_blueprint(opinions_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(access_bp)
app.register_blueprint(opinions_api_bp)
app.register_blueprint(auth_api_bp)
app.register_blueprint(admin_api_bp)


