#!/usr/bin/python
"""Defines the Place class."""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

class Place(BaseModel, Base):
    """Represents a Place."""

    if models.storage_t == 'db':
        __tablename__ = 'places'

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secondary="place_amenity", backref="places")

        if models.storage_t == 'db':
            place_amenity = Table('place_amenity', Base.metadata,
                                  Column('place_id', String(60), ForeignKey('places.id'),
                                         primary_key=True, nullable=False),
                                  Column('amenity_id', String(60), ForeignKey('amenities.id'),
                                         primary_key=True, nullable=False))

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Getter attribute that returns the list of Review instances."""
            return [review for review in models.storage.all("Review").values() if review.place_id == self.id]

        @property
        def amenities(self):
            """Getter attribute that returns the list of Amenity instances."""
            return [amenity for amenity in models.storage.all("Amenity").values() if amenity.place_id == self.id]

    def __init__(self, *args, **kwargs):
        """Initializes Place."""
        super().__init__(*args, **kwargs)

