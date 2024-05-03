#!/usr/bin/python3
""" Module to handle JSON file """
import json
from os.path import isfile
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Class to handle JSON file storage."""

    __file_path = "file.json"
    __objects = {}

    @staticmethod
    def constants():
        """Return a list of constant values."""
        return ['id', 'created_at', 'updated_at']

    def all(self):
        """Return the dictionary '__objects'."""
        return self.__class__.__objects

    def new(self, obj):
        """Add a BaseModel instance to '__objects'."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__class__.__objects[key] = obj

    def save(self):
        """Serialize '__objects' to the JSON file."""
        with open(self.__class__.__file_path, 'w', encoding='utf-8') as f:
            json.dump({k: v.to_dict() for k, v in self.__class__.__objects.items()}, f)

    def delete(self, class_name, obj_id):
        """Delete a BaseModel instance from '__objects' by id."""
        key = "{}.{}".format(class_name, obj_id)
        if key in self.__class__.__objects:
            del self.__class__.__objects[key]

    def reload(self):
        """Read the JSON file, create respective BaseModel instances, and store each one in '__objects'."""
        if not isfile(self.__class__.__file_path):
            return

        with open(self.__class__.__file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for k, v in data.items():
                obj = self.create_obj(v['__class__'], v)
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                self.__class__.__objects[key] = obj

    @staticmethod
    def create_obj(class_name, values=None):
        """Create an instance of a class dynamically."""
        classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }
        cls = classes.get(class_name)
        if cls and values:
            return cls(**values)
        return None

    @staticmethod
    def auto_cast(value):
        """Cast a given input to int, float, or str."""
        try:
            return int(value)
        except ValueError:
            pass

        try:
            return float(value)
        except ValueError:
            return str(value)

