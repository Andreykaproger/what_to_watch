from flask import Blueprint

opinions_bp = Blueprint(
    'opinions', __name__,
)

from . import routes