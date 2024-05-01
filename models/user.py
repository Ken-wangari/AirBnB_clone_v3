#!/usr/bin/python3
"""This holds the class"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """The representation of a user, class """
    __tablename__ = 'users' if models.storage_t == 'db' else None

    email = Column(String(128), nullable=False) if models.storage_t == 'db' else ""
    password = Column(String(128), nullable=False) if models.storage_t == 'db' else ""
    first_name = Column(String(128), nullable=True) if models.storage_t == 'db' else ""
    last_name = Column(String(128), nullable=True) if models.storage_t == 'db' else ""

    places = relationship("Place", backref="user", cascade="all, delete-orphan") if models.storage_t == 'db' else []
    reviews = relationship("Review", backref="user", cascade="all, delete-orphan") if models.storage_t == 'db' else []

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

