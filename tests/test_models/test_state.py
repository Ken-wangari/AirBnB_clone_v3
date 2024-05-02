#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

from datetime import datetime
import inspect
import models
from models import state
from models.base_model import BaseModel
import pep8
import unittest

State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_functions = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNot(state.__doc__, None,
                         "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1,
                        "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNot(State.__doc__, None,
                         "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1,
                        "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for name, func in self.state_functions:
            with self.subTest(name=name):
                self.assertIsNotNone(func.__doc__,
                                     f"{name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1,
                                f"{name} method needs a docstring")


class TestState(unittest.TestCase):
    """Test the State class"""

    def setUp(self):
        """Set up an instance of State for testing"""
        self.state = State()

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        self.assertIsInstance(self.state, BaseModel)
        self.assertTrue(hasattr(self.state, "id"))
        self.assertTrue(hasattr(self.state, "created_at"))
        self.assertTrue(hasattr(self.state, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's an empty string"""
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(self.state.name, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attrs"""
        new_dict = self.state.to_dict()
        self.assertIsInstance(new_dict, dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr, value in self.state.__dict__.items():
            if attr != "_sa_instance_state":
                self.assertIn(attr, new_dict)
                self.assertEqual(value, new_dict[attr])
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = self.state.to_dict()
        self.assertEqual(new_dict["__class__"], "State")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(new_dict["created_at"], self.state.created_at.strftime(t_format))
        self.assertEqual(new_dict["updated_at"], self.state.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        string = "[State] ({}) {}".format(self.state.id, self.state.__dict__)
        self.assertEqual(string, str(self.state))

