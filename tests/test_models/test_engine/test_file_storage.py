#!/usr/bin/python3
"""
Contains the TestFileStorageDocs and TestFileStorage classes
"""

import os
import json
import pep8
import unittest
import inspect
from datetime import datetime
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

FileStorage = file_storage.FileStorage
TEST_CLASSES = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
                "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_funcs = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNotNone(file_storage.__doc__, "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1, "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNotNone(FileStorage.__doc__, "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1, "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func_name, func in self.fs_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        objects_dict = storage.all()
        self.assertIsInstance(objects_dict, dict)
        self.assertIs(objects_dict, storage._FileStorage__objects)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        original_objects = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for class_name, model_class in TEST_CLASSES.items():
            instance = model_class()
            instance_key = f"{instance.__class__.__name__}.{instance.id}"
            storage.new(instance)
            test_dict[instance_key] = instance
            self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = original_objects

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        objects_dict = {}
        for class_name, model_class in TEST_CLASSES.items():
            instance = model_class()
            instance_key = f"{instance.__class__.__name__}.{instance.id}"
            objects_dict[instance_key] = instance
        original_objects = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = objects_dict
        storage.save()
        FileStorage._FileStorage__objects = original_objects
        for key, value in objects_dict.items():
            objects_dict[key] = value.to_dict()
        expected_json = json.dumps(objects_dict)
        with open("file.json", "r") as f:
            actual_json = f.read()
        self.assertEqual(json.loads(expected_json), json.loads(actual_json))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_get(self):
        """Test that the get method properly retrieves objects"""
        storage = FileStorage()
        self.assertIsNone(storage.get("User", "blah"))
        self.assertIsNone(storage.get("blah", "blah"))
        new_user = User()
        new_user.save()
        self.assertIs(storage.get("User", new_user.id), new_user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_count(self):
        """Test count method of FileStorage"""
        storage = FileStorage()
        initial_length = len(storage.all())
        self.assertEqual(storage.count(), initial_length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), initial_length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)


if __name__ == "__main__":
    unittest.main()

