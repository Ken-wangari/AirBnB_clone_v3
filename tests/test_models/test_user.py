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

User = user.User


class TestUserDocs(unittest.TestCase):
    """Tests to check the documentation and style of User class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.user_functions = inspect.getmembers(User, inspect.isfunction)

    def test_pep8_conformance_user(self):
        """Test that models/user.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_user(self):
        """Test that tests/test_models/test_user.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_user.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_user_module_docstring(self):
        """Test for the user.py module docstring"""
        self.assertIsNot(user.__doc__, None,
                         "user.py needs a docstring")
        self.assertTrue(len(user.__doc__) >= 1,
                        "user.py needs a docstring")

    def test_user_class_docstring(self):
        """Test for the User class docstring"""
        self.assertIsNot(User.__doc__, None,
                         "User class needs a docstring")
        self.assertTrue(len(User.__doc__) >= 1,
                        "User class needs a docstring")

    def test_user_func_docstrings(self):
        """Test for the presence of docstrings in User methods"""
        for name, func in self.user_functions:
            with self.subTest(name=name):
                self.assertIsNotNone(func.__doc__,
                                     f"{name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1,
                                f"{name} method needs a docstring")


class TestUser(unittest.TestCase):
    """Test the User class"""

    def setUp(self):
        """Set up an instance of User for testing"""
        self.user = User()

    def test_is_subclass(self):
        """Test that User is a subclass of BaseModel"""
        self.assertIsInstance(self.user, BaseModel)
        self.assertTrue(hasattr(self.user, "id"))
        self.assertTrue(hasattr(self.user, "created_at"))
        self.assertTrue(hasattr(self.user, "updated_at"))

    def test_email_attr(self):
        """Test that User has attr email, and it's an empty string"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertEqual(self.user.email, "")

    def test_password_attr(self):
        """Test that User has attr password, and it's an empty string"""
        self.assertTrue(hasattr(self.user, "password"))
        self.assertEqual(self.user.password, "")

    def test_first_name_attr(self):
        """Test that User has attr first_name, and it's an empty string"""
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertEqual(self.user.first_name, "")

    def test_last_name_attr(self):
        """Test that User has attr last_name, and it's an empty string"""
        self.assertTrue(hasattr(self.user, "last_name"))
        self.assertEqual(self.user.last_name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attrs"""
        new_dict = self.user.to_dict()
        self.assertIsInstance(new_dict, dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr, value in self.user.__dict__.items():
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_dict)
                self.assertEqual(value, new_dict[attr])
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = self.user.to_dict()
        self.assertEqual(new_dict["__class__"], "User")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(new_dict["created_at"], self.user.created_at.strftime(t_format))
        self.assertEqual(new_dict["updated_at"], self.user.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        string = "[User] ({}) {}".format(self.user.id, self.user.__dict__)
        self.assertEqual(string, str(self.user))

