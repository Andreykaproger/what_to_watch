from flask import render_template, jsonify

from . import db


class InvalidAPIUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


def register_error_handlers(app):

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(InvalidAPIUsage)
    def invalid_api_usage(error):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/404.html')

