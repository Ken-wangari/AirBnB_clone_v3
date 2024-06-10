#!/usr/bin/python3
"""Unit tests for User class"""

import unittest
from unittest.mock import patch
from os import remove
from models.user import User
from models.base_model import BaseModel


class TestInstanceUser(unittest.TestCase):
    """Class for unittests of instance check"""

    def tearDown(self):
        """Tear down for all methods"""
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_instance(self):
        """Checks if user is instance of base_model"""
        user = User()
        self.assertIsInstance(user, BaseModel)

    def test_instance_args(self):
        """Checks if user with args is instance of base_model"""
        user = User(123, "Hello", ["World"])
        self.assertIsInstance(user, BaseModel)

    def test_instance_kwargs(self):
        """Checks if user with kwargs is instance of base_model"""
        user_data = {"name": "Holberton"}
        user = User(**user_data)
        self.assertIsInstance(user, BaseModel)


class TestClassAttrsUser(unittest.TestCase):
    """Class for checking if class attributes were set correctly"""

    def tearDown(self):
        """Tear down for all methods"""
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_correct_class_attrs(self):
        """Checks if class attributes are present and initialized"""
        user = User()
        attrs = ["email", "password", "first_name", "last_name"]
        for attr in attrs:
            self.assertTrue(hasattr(user, attr))
            self.assertEqual(getattr(user, attr), "")

    def test_set_attr(self):
        """Check setting instance attributes and accessing class attributes"""
        user = User()
        attrs = ["email", "password", "first_name", "last_name"]
        values = ["123@hmail.com", "password", "Larry", "Page"]
        for attr, value in zip(attrs, values):
            setattr(user, attr, value)
        for attr, value in zip(attrs, values):
            self.assertEqual(getattr(user, attr), value)
        for attr in attrs:
            self.assertEqual(getattr(user.__class__, attr), "")

