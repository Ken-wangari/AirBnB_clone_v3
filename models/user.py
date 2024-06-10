#!/usr/bin/python3

"""Module for the User class."""

from models.base_model import BaseModel


class User(BaseModel):
    """User class to represent user personal information."""

    def __init__(self, *args, **kwargs):
        """Initialize User class."""
        super().__init__(*args, **kwargs)
        self.email = ""
        self.password = ""
        self.first_name = ""
        self.last_name = ""

