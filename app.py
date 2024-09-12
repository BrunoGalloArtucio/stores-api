"""App File"""

import os

from flask import Flask
from flask_smorest import Api
from exceptions import ApiErrorException
from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint
from resources.tags import blp as TagsBlueprint
from db import db


def create_app(db_url=None):
    """Create Flask App"""

    app = Flask(__name__)

    # Flask config that says that if there's an exception that occurs hidden inside an
    # extension of flask,to propagate it into the main app so that we can see it
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Flask Stores API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/openapi-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL",
        "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(TagsBlueprint)

    @app.errorhandler(ApiErrorException)
    def handle_api_error(err: ApiErrorException):
        """Error handler"""
        response = {
            "code": err.code,
            "status": err.status,
            "message": err.message,
            "detail": err.detail,
        }

        return response, err.code

    return app
