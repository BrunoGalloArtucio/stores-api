"""Items Model File"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import db


class ItemModel(db.Model):
    """Item Model"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship(
        "TagModel", back_populates="items", secondary="items_tags")
