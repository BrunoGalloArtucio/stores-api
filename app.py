"""App File"""

import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from exceptions import ApiErrorException
from resources.items import blp as ItemsBlueprint
from resources.stores import blp as StoresBlueprint
from resources.tags import blp as TagsBlueprint
from resources.users import blp as UsersBlueprint
from db import db
from blocklist import BLOCKLIST


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

    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY",
        "95088854782557170340987083085166124607"
    )
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwy_payload):
        return jwy_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has been revoked via log out",
                "status": "Unauthorized"
            }),
            401
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwy_payload):
        return (
            jsonify({
                "message": "The token is not fresh",
                "status": "Unauthorized"
            }),
            401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "The token has expired",
                "status": "Unauthorized"
            }),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": "Signature verification failed",
                "status": "Unauthorized"
            }),
            401
        )

    @jwt.unauthorized_loader
    def unauthorized_loader_callback(error):
        return (
            jsonify({
                "message": "Request does not contain access token",
                "status": "Unauthorized"
            }),
            401
        )

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemsBlueprint)
    api.register_blueprint(StoresBlueprint)
    api.register_blueprint(TagsBlueprint)
    api.register_blueprint(UsersBlueprint)

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
