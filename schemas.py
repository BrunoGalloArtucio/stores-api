"""Validation Schemas"""

from marshmallow import Schema, fields, validate


class PlainItemSchema(Schema):
    """Validation schema for item creation"""
    # dump_only means it's only expected on the response bodies
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()
    price = fields.Float(required=True, validate=validate.Range(min=0.01))


class PlainStoreSchema(Schema):
    """Validation schema for stores"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))


class PlainTagSchema(Schema):
    """Validation schema for tags"""
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3))


class StoreSchema(PlainStoreSchema):
    """Validation schema for stores"""
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)


class ItemSchema(PlainItemSchema):
    """Validation schema for items"""
    # load_only means it's only expected on the request bodies
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema), dump_only=True)


class TagSchema(PlainTagSchema):
    """Validation schema for tags"""
    # load_only means it's only expected on the request bodies
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema), dump_only=True)


class ItemUpdateSchema(Schema):
    """Validation schema for item creation"""
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str()
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    store_id = fields.Int()


class TagAndItemSchema(Schema):
    """Used to return information about the related item and tag"""
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)


class UserSchema(Schema):
    """User Schema"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(
        required=True, validate=validate.Length(min=8), load_only=True)
