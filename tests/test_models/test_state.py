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

# Alias for better readability
State = state.State


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_methods = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state(self):
        """Test that models/state.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in models/state.py"
        )

    def test_pep8_conformance_test_state(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(
            result.total_errors, 0,
            "Found code style errors (and warnings) in tests/test_models/test_state.py"
        )

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNotNone(state.__doc__, "state.py needs a docstring")
        self.assertTrue(len(state.__doc__) >= 1, "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNotNone(State.__doc__, "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1, "State class needs a docstring")

    def test_state_method_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for method_name, method_obj in self.state_methods:
            with self.subTest(method_name=method_name):
                self.assertIsNotNone(
                    method_obj.__doc__,
                    f"{method_name} method needs a docstring"
                )
                self.assertTrue(
                    len(method_obj.__doc__) >= 1,
                    f"{method_name} method needs a docstring"
                )


class TestState(unittest.TestCase):
    """Test the State class"""

    def test_is_subclass(self):
        """Test that State is a subclass of BaseModel"""
        state_instance = State()
        self.assertIsInstance(state_instance, BaseModel)
        self.assertTrue(hasattr(state_instance, "id"))
        self.assertTrue(hasattr(state_instance, "created_at"))
        self.assertTrue(hasattr(state_instance, "updated_at"))

    def test_name_attr(self):
        """Test that State has attribute name, and it's an empty string"""
        state_instance = State()
        self.assertTrue(hasattr(state_instance, "name"))
        if models.storage_t == 'db':
            self.assertIsNone(state_instance.name)
        else:
            self.assertEqual(state_instance.name, "")

    def test_to_dict_creates_dict(self):
        """Test if to_dict method creates a dictionary with proper attrs"""
        state_instance = State()
        new_dict = state_instance.to_dict()
        self.assertEqual(type(new_dict), dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr in state_instance.__dict__:
            with self.subTest(attr=attr):
                if attr != "_sa_instance_state":
                    self.assertIn(attr, new_dict)
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test if values in dictionary returned from to_dict are correct"""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        state_instance = State()
        new_dict = state_instance.to_dict()
        self.assertEqual(new_dict["__class__"], "State")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(
            new_dict["created_at"], state_instance.created_at.strftime(time_format)
        )
        self.assertEqual(
            new_dict["updated_at"], state_instance.updated_at.strftime(time_format)
        )

    def test_str(self):
        """Test if the str method has the correct output"""
        state_instance = State()
        string = "[State] ({}) {}".format(state_instance.id, state_instance.__dict__)
        self.assertEqual(string, str(state_instance))


if __name__ == "__main__":
    unittest.main()

