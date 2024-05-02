#!/usr/bin/python3
"""
Contains the TestUserDocs classes
"""

from datetime import datetime
import inspect
import models
from models import user
from models.base_model import BaseModel
import pep8
import unittest

# Alias for better readability
User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_methods = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/user.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in models/user.py"
        )

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in tests/test_models/test_user.py"
        )

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNotNone(user.__doc__, "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1, "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNotNone(User.__doc__, "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1, "User class needs a docstring")

    def test_user_method_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for method_name, method_obj in self.user_methods:
            with self.subTest(method_name=method_name):
                self.assertIsNotNone(
                    method_obj.__doc__,
                    f"{method_name} method needs a docstring"
                )
                self.assertTrue(
                    len(method_obj.__doc__) >= 1,
                    f"{method_name} method needs a docstring"
                )


class TestUser(unittest.TestCase):
    """Test the User class"""

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        user_instance = User()
        self.assertIsInstance(user_instance, BaseModel)
        self.assertTrue(hasattr(user_instance, "id"))
        self.assertTrue(hasattr(user_instance, "created_at"))
        self.assertTrue(hasattr(user_instance, "updated_at"))

    def test_attributes_default_values(self):
        """Test default values of User attributes"""
        user_instance = User()
        attributes = ["email", "password", "first_name", "last_name"]
        for attr in attributes:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(user_instance, attr))
                if models.storage_t == 'db':
                    self.assertIsNone(getattr(user_instance, attr))
                else:
                    self.assertEqual(getattr(user_instance, attr), "")

    def test_to_dict_creates_dict(self):
        """Test if to_dict method creates a dictionary with proper attrs"""
        user_instance = User()
        new_dict = user_instance.to_dict()
        self.assertEqual(type(new_dict), dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr in user_instance.__dict__:
            with self.subTest(attr=attr):
                if attr != "_sa_instance_state":
                    self.assertIn(attr, new_dict)
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test if values in dictionary returned from to_dict are correct"""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        user_instance = User()
        new_dict = user_instance.to_dict()
        self.assertEqual(new_dict["__class__"], "User")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(
            new_dict["created_at"], user_instance.created_at.strftime(time_format)
        )
        self.assertEqual(
            new_dict["updated_at"], user_instance.updated_at.strftime(time_format)
        )

    def test_str(self):
        """Test if the str method has the correct output"""
        user_instance = User()
        string = "[User] ({}) {}".format(user_instance.id, user_instance.__dict__)
        self.assertEqual(string, str(user_instance))


if __name__ == "__main__":
    unittest.main()

