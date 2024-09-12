"""Store resource"""

from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import create_access_token
from exceptions import ApiErrorException
from schemas import UserSchema
from models import UserModel
from db import db

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route('/register')
class Register(MethodView):
    """Users method view"""

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """POST users"""
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        try:
            db.session.add(user)
            db.session.commit()
            return user

        except IntegrityError as e:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "username already in use",
                {"user": user_data, "error": str(e)}
            ) from IntegrityError

        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not create user",
                {"user": user_data, "error": str(e)}
            ) from SQLAlchemyError


@blp.route('/login')
class UserLogIn(MethodView):
    """Log in method view"""

    @blp.arguments(UserSchema)
    @blp.response(200)
    def post(self, user_data):
        """POST users"""
        user = UserModel.query.filter(
            UserModel.username == user_data["username"],
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}

        raise ApiErrorException(
            403,
            "Unauthorized",
            "Invalid username/password combination",
            {}
        )


@blp.route('/users/<int:user_id>')
class User(MethodView):
    """user method view"""

    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user by id"""
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.response(204)
    def delete(self, user_id):
        """Delete user by id"""
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
