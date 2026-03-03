from flask import Blueprint

access_bp = Blueprint(
    'access', __name__,
)

from . import routes