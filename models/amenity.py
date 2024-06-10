#!/usr/bin/python3

"""Definition of the Amenity class."""

from models.base_model import BaseModel

class Amenity(BaseModel):
    """Amenity class to represent amenities of a place."""
    def __init__(self, *args, **kwargs):
        """Initialize Amenity class."""
        super().__init__(*args, **kwargs)
        self.name = ""

