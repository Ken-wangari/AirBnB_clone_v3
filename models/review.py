#!/usr/bin/python3

"""Module for the Review class."""

from models.base_model import BaseModel


class Review(BaseModel):
    """Review class to represent review information."""

    def __init__(self, *args, **kwargs):
        """Initialize Review class."""
        super().__init__(*args, **kwargs)
        self.place_id = ""
        self.user_id = ""
        self.text = ""

