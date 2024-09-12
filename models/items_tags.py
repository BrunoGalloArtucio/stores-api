"""Items Tags Many to Many"""
from sqlalchemy import Column, Integer, ForeignKey
from db import db


class ItemsTagsModel(db.Model):
    """Items Tags Many to Many Modal"""
    __tablename__ = "items_tags"

    id = Column(Integer, primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
