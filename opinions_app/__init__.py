from apiflask import APIFlask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

from settings import Config


db = SQLAlchemy()
jwt = JWTManager()
login_manager = LoginManager()
migrate = Migrate()


def create_app(config_class=Config):

    app = APIFlask(
        __name__,
        title="What to Watch API",
        version="1.0",
        docs_path="/api/docs"
    )

    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = "access.login_view"

    from .models import User, TokenBlockList

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        token = TokenBlockList.query.filter_by(jti=jti).first()

        return token is not None

    from .error_handlers import register_error_handlers
    from .utils import decorators
    from .utils.cli_commands import register_cli

    register_error_handlers(app)
    register_cli(app)

    from .users import users_bp
    from .opinions import opinions_bp
    from .admin.routes import admin_bp
    from .access_managment.routes import access_bp
    from .api.opinions_api import opinions_api_bp
    from .api.auth_api import auth_api_bp
    from .api.admin_api import admin_api_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(opinions_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(access_bp)
    app.register_blueprint(opinions_api_bp)
    app.register_blueprint(auth_api_bp)
    app.register_blueprint(admin_api_bp)

    return app