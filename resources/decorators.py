"""Decorators"""
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt
from exceptions import ApiErrorException


def admin_required(func):
    """Decorator to check if the user has admin privileges."""
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        # Retrieve the JWT from the request
        jwt = get_jwt()

        # Check if the 'is_admin' field is present and True
        if not jwt.get("is_admin"):
            # Raise your custom exception if the user is not an admin
            raise ApiErrorException(
                403,
                "Forbidden",
                "Admin privilege required",
                {}
            )

        # Call the original function if the user is an admin
        return func(*args, **kwargs)

    return wrapper
