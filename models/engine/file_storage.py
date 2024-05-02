#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    def __init__(self):
        """Initializes FileStorage"""
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects"""
        if cls:
            cls_name = cls.__name__
            return {key: obj for key, obj in self.__objects.items() if type(obj).__name__ == cls_name}
        return self.__objects

    def new(self, obj):
        """Adds a new object to __objects"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w') as file:
            json.dump(json_dict, file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as file:
                json_dict = json.load(file)
                self.__objects = {}
                for key, val in json_dict.items():
                    class_name = val['__class__']
                    cls = eval(class_name)
                    obj = cls(**val)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes obj from __objects"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
            self.save()

    def close(self):
        """Calls reload to deserialize JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Retrieves an object by class name and ID"""
        key = "{}.{}".format(cls.__name__, id)
        return self.__objects.get(key)

    def count(self, cls=None):
        """Counts the number of objects in storage"""
        if cls:
            cls_name = cls.__name__
            return sum(1 for obj in self.__objects.values() if type(obj).__name__ == cls_name)
        return len(self.__objects)
