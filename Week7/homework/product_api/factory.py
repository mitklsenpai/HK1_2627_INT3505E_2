from flask import Flask

# Tái sử dụng lab1 cho Product model/blueprint (đơn giản, không copy lại)
import sys, pathlib
_lab1 = pathlib.Path(__file__).resolve().parent.parent / "lab1" / "product_api"
sys.path.insert(0, str(_lab1))

from product_api.api.products import products_bp
from product_api.extensions import db as lab1_db

from .extensions import db, migrate
from .config import DefaultConfig
from .errors import register_error_handlers
from .logging_config import configure_logging
from .api.orders import orders_bp
from .api.health import health_bp
from .models import Product  # model Homework tự khai báo (chung bảng)


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

    # Đăng ký từ lab1 + homework
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)
    return app