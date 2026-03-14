from apiflask import APIBlueprint


opinions_api_bp = APIBlueprint(
    "opinions_api",
    __name__,
    url_prefix="/api",
    tag='Мнения о фильмах'
)

auth_api_bp = APIBlueprint(
    "auth_api",
    __name__,
    url_prefix="/api/auth/",
    tag='Регистрация/Авторизация'
)

admin_api_bp = APIBlueprint(
    "admin_panel",
    __name__,
    url_prefix="/api/admin",
    tag='Панель администратора'
)

from . import auth, opinions, admin

