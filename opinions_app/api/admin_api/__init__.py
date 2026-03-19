from apiflask import APIBlueprint


admin_api_bp = APIBlueprint(
    "admin_panel",
    __name__,
    url_prefix="/api/admin",
    tag='Панель администратора'
)

from . import opinions, users, services