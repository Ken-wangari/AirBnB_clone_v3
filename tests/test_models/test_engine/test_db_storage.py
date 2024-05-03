#!/usr/bin/python3
"""
Contains test cases for DBStorage class and its documentation
"""

import os
import unittest
import pep8
import inspect
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_funcs = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test PEP8 conformance"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py', 'tests/test_models/test_engine/test_db_storage.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found")

    def test_db_storage_module_docstring(self):
        """Test for the DBStorage module docstring"""
        self.assertIsNotNone(DBStorage.__doc__, "DBStorage module needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1, "DBStorage module needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNotNone(DBStorage.__doc__, "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1, "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func_name, func in self.dbs_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Not testing database storage")
    def test_get_method(self):
        """Test get method of DBStorage"""
        new_state = State(name="New York")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertIs(DBStorage().get("State", new_state.id), new_state)
        self.assertIsNone(DBStorage().get("State", "blah"))
        self.assertIsNone(DBStorage().get("blah", "blah"))
        self.assertIs(DBStorage().get("User", new_user.id), new_user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Not testing database storage")
    def test_count_method(self):
        """Test count method of DBStorage"""
        initial_count = DBStorage().count()
        self.assertEqual(DBStorage().count("Blah"), 0)
        new_state = State(name="Florida")
        new_state.save()
        new_user = User(email="bob@foobar.com", password="password")
        new_user.save()
        self.assertEqual(DBStorage().count("State"), initial_count + 1)
        self.assertEqual(DBStorage().count(), initial_count + 2)


if __name__ == "__main__":
    unittest.main()

