from apiflask import APIBlueprint


opinions_api_bp = APIBlueprint(
    "opinions_api",
    __name__,
    url_prefix="/api",
    tag='Мнения о фильмах'
)

from . import opinions