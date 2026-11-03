import json
import logging
import sys
import time
import uuid

from flask import g, has_request_context, request


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "level": record.levelname,
            "event": record.getMessage(),
        }
        for key in ("request_id", "method", "path", "status", "ms"):
            value = getattr(record, key, None)
            if value is not None:
                payload[key] = value
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(app):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    app.logger.handlers = [handler]
    app.logger.setLevel(app.config["LOG_LEVEL"])

    @app.before_request
    def _start():
        g.request_id = request.headers.get("X-Request-Id", uuid.uuid4().hex)
        g.started_at = time.perf_counter()

    @app.after_request
    def _done(resp):
        resp.headers["X-Request-Id"] = g.get("request_id", "-")
        app.logger.info(
            "request",
            extra={
                "request_id": g.get("request_id", "-"),
                "method": request.method,
                "path": request.path,
                "status": resp.status_code,
                "ms": int((time.perf_counter() - g.get("started_at", time.perf_counter())) * 1000),
            },
        )
        return resp
