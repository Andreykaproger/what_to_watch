from flask import Blueprint

admin_bp = Blueprint(
    "admin", __name__,
    url_prefix="/admin/dashboard"
)

from . import dashboard_routes
from . import opinion_routes
from . import user_routes