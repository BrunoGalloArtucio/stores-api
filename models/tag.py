"""Stores Model File"""
from sqlalchemy import Column, Integer, String, ForeignKey
from db import db


class TagModel(db.Model):
    """Store Model"""
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship(
        "ItemModel", back_populates="tags", secondary="items_tags")
