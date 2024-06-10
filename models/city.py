#!/usr/bin/python3

"""Module for the City class."""

from models.base_model import BaseModel


class City(BaseModel):
    """City class to represent city information."""

    def __init__(self, *args, **kwargs):
        """Initialize City class."""
        super().__init__(*args, **kwargs)
        self.state_id = ""
        self.name = ""

