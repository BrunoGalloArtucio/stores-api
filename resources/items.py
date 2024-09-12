"""Store resource"""

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint
from exceptions import ApiErrorException
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db

blp = Blueprint("items", __name__, description="Operation on items")


@blp.route('/items')
class Items(MethodView):
    """Items method view"""

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        """GET items"""
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        """POST items"""
        item = ItemModel(**item_data)

        validate_item_name(item_data["name"], item_data["store_id"])

        try:
            db.session.add(item)
            db.session.commit()
            return item
        except IntegrityError as e:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Item name already in use",
                {"item": item_data, "error": str(e)}
            ) from IntegrityError
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not create item",
                {"item": item_data, "error": str(e)}
            ) from SQLAlchemyError


@blp.route('/items/<int:item_id>')
class Item(MethodView):
    """Item method view"""

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        """Get item by id"""
        item = ItemModel.query.get_or_404(item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        """PUT items"""
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            validate_item_name(item_data["name"], item.store_id, item.id)
        else:
            item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
            return item
        except IntegrityError as e:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Item name already in use",
                {"item": item_data, "error": str(e)}
            ) from SQLAlchemyError
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not create item",
                {"item": item_data, "error": str(e)}
            ) from SQLAlchemyError

    @blp.response(204)
    def delete(self, item_id):
        """Delete item by id"""
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()


def validate_item_name(item_name: str, store_id: str, current_item_id=None):
    """Checks an item name is unique for store"""
    existing_item = ItemModel.query.filter(
        ItemModel.store_id == store_id, ItemModel.name == item_name
    ).first()

    if existing_item and (current_item_id is None or current_item_id != existing_item.id):
        print("Existing item:")
        print(existing_item.id)

        raise ApiErrorException(
            422,
            "Unprocessable Entity",
            "Item name already in use for store",
            {"item_name": item_name}
        ) from SQLAlchemyError
