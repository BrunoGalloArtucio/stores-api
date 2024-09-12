"""Stores Model File"""
from sqlalchemy import Column, Integer, String
from db import db


class StoreModel(db.Model):
    """Store Model"""
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)

    items = db.relationship(
        "ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

    tags = db.relationship(
        "TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")
