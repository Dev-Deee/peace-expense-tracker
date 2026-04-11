from flask import jsonify
from app.exceptions.api_exception import APIException
from marshmallow import ValidationError


def register_error_handlers(app):

    @app.errorhandler(APIException)
    def handle_api_exception(e):
        return jsonify({"error": e.message}), e.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"error": e.messages}), 400

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal server error"}), 500