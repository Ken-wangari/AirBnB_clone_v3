#!/usr/bin/python
"""Defines the City class."""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class City(BaseModel, Base):
    """Represents a City."""

    __tablename__ = 'cities' if models.storage_t == "db" else None

    if models.storage_t == "db":
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="city")
    else:
        state_id = ""
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes City."""
        super().__init__(*args, **kwargs)

