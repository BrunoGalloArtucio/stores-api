"""Tags View"""
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models import TagModel, StoreModel, ItemModel
from schemas import PlainTagSchema, TagSchema
from exceptions import ApiErrorException
from db import db

blp = Blueprint("tags", __name__, description="Operation on tags")


@blp.route('/stores/<int:store_id>/tags')
class Tags(MethodView):
    """Item method view"""

    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        """Get tags by store id"""
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

    @blp.arguments(PlainTagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        """POST tags"""
        tag = TagModel(**tag_data, store_id=store_id)

        existing_tag = TagModel.query.filter(
            TagModel.store_id == store_id, TagModel.name == tag_data["name"]
        ).first()

        if existing_tag:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Tag name already in use for store",
                {"tag": tag_data}
            ) from SQLAlchemyError

        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except IntegrityError as e:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Tag name already in use",
                {"tag": tag_data, "error": str(e)}
            ) from IntegrityError
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not create tag",
                {"tag": tag_data, "error": str(e)}
            ) from SQLAlchemyError


@blp.route('/tags/<int:tag_id>')
class Tag(MethodView):
    """Tag Method view"""

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        """Get tag by id"""
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(204, description="Deletes a tag if no item is tagged with it")
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        422,
        description="Returned if the tag is assigned to one or more items"
    )
    def delete(self, tag_id):
        """Delete tag by id"""
        tag = TagModel.query.get_or_404(tag_id)
        if tag.items:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Cannot delete tag. Tag is in use by items",
                {"tag": tag}
            )

        db.session.delete(tag)
        db.session.commit()


@blp.route('/item/<int:item_id>/tags/<int:tag_id>')
class LinkTagsToItem(MethodView):
    """Link Tags To Item Method view"""

    @blp.response(204)
    def post(self, item_id, tag_id):
        """Link item and tag"""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.append(tag)

        if item.store_id != tag.store_id:
            raise ApiErrorException(
                422,
                "Unprocessable Entity",
                "Could not link item to tag since they belong to different stores",
                {"item_id": item_id, "tag_id": tag_id}
            )

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not link item to tag",
                {"item_id": item_id, "tag_id": tag_id, "error": str(e)}
            ) from SQLAlchemyError

    @blp.response(204)
    def delete(self, item_id, tag_id):
        """Remove tag from item"""
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            raise ApiErrorException(
                500,
                "Internal Server Error",
                "Could not unlink item to tag",
                {"item_id": item_id, "tag_id": tag_id, "error": str(e)}
            ) from SQLAlchemyError
