from flask import jsonify
from werkzeug.exceptions import HTTPException


class ApiError(Exception):
    status_code = 500
    code = "internal_error"

    def __init__(self, message="", code=None, status=None):
        super().__init__(message)
        if code:
            self.code = code
        if status:
            self.status_code = status
        self.message = message


class NotFound(ApiError):
    status_code = 404
    code = "not_found"


class Conflict(ApiError):
    status_code = 409
    code = "conflict"


class OutOfStock(ApiError):
    status_code = 409
    code = "out_of_stock"


def register_error_handlers(app):
    from marshmallow import ValidationError

    @app.errorhandler(ApiError)
    def _on_api(err):
        return jsonify({"error": err.code, "detail": err.message}), err.status_code

    @app.errorhandler(ValidationError)
    def _on_validation(err):
        return jsonify({"error": "validation_error", "detail": err.messages}), 422

    @app.errorhandler(HTTPException)
    def _on_http(err):
        return (
            jsonify(
                {
                    "error": err.name.lower().replace(" ", "_"),
                    "detail": err.description,
                }
            ),
            err.code,
        )

    @app.errorhandler(Exception)
    def _on_unhandled(err):
        app.logger.exception("unhandled")
        return jsonify({"error": "internal_error", "detail": "unexpected server error"}), 500
