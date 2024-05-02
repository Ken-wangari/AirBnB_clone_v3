#!/usr/bin/python
"""Defines the Amenity class."""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String

class Amenity(BaseModel, Base):
    """Represents an Amenity."""
    
    __tablename__ = 'amenities' if models.storage_t == 'db' else None

    if models.storage_t == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes Amenity."""
        super().__init__(*args, **kwargs)

