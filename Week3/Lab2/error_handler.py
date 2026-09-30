from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

class ProblemError(Exception):
    def __init__(self, status, title, detail=None):
        self.status = status
        self.title = title
        self.detail = detail

def initErrorHandler(app):
    @app.errorhandler(ProblemError)
    def handle_problem_error(error):
        response = {
            "type": "about:blank",
            "title": error.title,
            "status": error.status
        }

        if error.detail:
            response["detail"] = error.detail

        return jsonify(response), error.status

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        return jsonify({
            "type": "about:blank",
            "title": error.name,
            "status": error.code,
            "detail": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        app.logger.exception(error)

        return jsonify({
            "type": "about:blank",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred"
        }), 500


# ví dụ về handler sẽ nhét luôn vào lab1 cho gọn + đỡ phải làm lại API
# ví dụ cụ thể ở file README.md cùng root với lab2