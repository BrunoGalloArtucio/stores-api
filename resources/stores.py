"""Store resource"""

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint
from exceptions import ApiErrorException
from schemas import StoreSchema
from models import StoreModel
from db import db

blp = Blueprint("stores", __name__, description="Operation on stores")


@blp.route('/stores')
class Stores(MethodView):
    """Stores method view"""

    @blp.response(200, StoreSchema(many=True))
    def get(self):
        """GET stores"""
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        """POST stores"""
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError as e:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Store name already in use",
                {"store": store_data, "error": str(e)}
            ) from IntegrityError
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not create item",
                {"store": store_data, "error": str(e)}
            ) from SQLAlchemyError
        return store


@blp.route('/stores/<string:store_id>')
class Store(MethodView):
    """Store method view"""

    @blp.response(200, StoreSchema)
    def get(self, store_id):
        """Get store by id"""
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.response(204)
    def delete(self, store_id):
        """Delete store by id"""
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
