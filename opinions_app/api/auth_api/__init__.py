from apiflask import APIBlueprint


auth_api_bp = APIBlueprint(
    "auth_api",
    __name__,
    url_prefix="/api/auth",
    tag='Регистрация/Авторизация'
)

from . import auth