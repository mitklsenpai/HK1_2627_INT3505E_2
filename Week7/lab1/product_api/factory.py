from flask import Flask

from .api import products_bp
from .config import DefaultConfig
from .errors import register_error_handlers
from .extensions import db, migrate
from .logging_config import configure_logging


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(DefaultConfig)
    if config is not None:
        if isinstance(config, dict):
            app.config.from_mapping(config)
        else:
            app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_logging(app)
    register_error_handlers(app)

    app.register_blueprint(products_bp)
    return app