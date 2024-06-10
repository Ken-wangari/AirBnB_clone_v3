#!/usr/bin/python3

"""Module for the State class."""

from models.base_model import BaseModel


class State(BaseModel):
    """State class to represent state information."""

    def __init__(self, *args, **kwargs):
        """Initialize State class."""
        super().__init__(*args, **kwargs)
        self.name = ""

