#!/usr/bin/python3

"""Module for the BaseModel class and utilities"""

from datetime import datetime
from models import storage
from uuid import uuid4 as uuid


class BaseModel:
    """BaseModel class to serve as the foundation for other models"""

    def __init__(self, *args, **kwargs):
        """Initialize a BaseModel instance"""
        if kwargs:
            self.set_by_kwargs(**kwargs)
        else:
            self.id = str(uuid())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    @staticmethod
    def isoparse(isoformat):
        """Parse a date from ISO format to datetime object"""
        return datetime.strptime(isoformat, "%Y-%m-%dT%H:%M:%S.%f")

    def set_by_kwargs(self, **kwargs):
        """Set properties by kwargs to a BaseModel instance"""
        for k, v in kwargs.items():
            if k == 'created_at' or k == 'updated_at':
                setattr(self, k, self.isoparse(v))
            elif k != '__class__':
                setattr(self, k, v)

    def save(self):
        """Save changes of a BaseModel instance and update JSON file"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return all info of a BaseModel instance as a dictionary"""
        return {
            **self.__dict__,
            '__class__': self.__class__.__name__,
            'updated_at': self.updated_at.isoformat(),
            'created_at': self.created_at.isoformat()
        }

    def __str__(self):
        """Print info of a BaseModel instance"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

