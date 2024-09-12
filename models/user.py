"""Users Model File"""
from sqlalchemy import Column, Integer, String
from db import db


class UserModel(db.Model):
    """User Model"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
