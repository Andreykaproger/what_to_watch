from . import app

from users import users_bp
from opinions import opinions_bp
from admin import admin_bp
from access_managment import access_bp

app.register_blueprint(users_bp)
app.register_blueprint(opinions_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(access_bp)


