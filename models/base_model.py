#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time_format = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.created_at = self.__parse_datetime(kwargs.get("created_at", None))
            self.updated_at = self.__parse_datetime(kwargs.get("updated_at", None))
            for key, value in kwargs.items():
                if key not in ["__class__", "id", "created_at", "updated_at"]:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id,
                                     self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["created_at"] = self.created_at.strftime(time_format)
        new_dict["updated_at"] = self.updated_at.strftime(time_format)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)

    @staticmethod
    def __parse_datetime(dt_str):
        """Parse datetime string to datetime object"""
        if isinstance(dt_str, str):
            return datetime.strptime(dt_str, time_format)
        return dt_str

