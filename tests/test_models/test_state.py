#!/usr/bin/python3
"""
Contains the TestStateDocs classes
"""

import unittest
import pep8
import inspect
from models.state import State
from models.base_model import BaseModel
import models


class TestStateDocs(unittest.TestCase):
    """Tests to check the documentation and style of State class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.state_funcs = inspect.getmembers(State, inspect.isfunction)

    def test_pep8_conformance_state_module(self):
        """Test that models/state.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/state.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in state module")

    def test_pep8_conformance_test_state_module(self):
        """Test that tests/test_models/test_state.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_state.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in test_state module")

    def test_state_module_docstring(self):
        """Test for the state.py module docstring"""
        self.assertIsNotNone(State.__doc__, "state.py needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1, "state.py needs a docstring")

    def test_state_class_docstring(self):
        """Test for the State class docstring"""
        self.assertIsNotNone(State.__doc__, "State class needs a docstring")
        self.assertTrue(len(State.__doc__) >= 1, "State class needs a docstring")

    def test_state_func_docstrings(self):
        """Test for the presence of docstrings in State methods"""
        for func_name, func in self.state_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestState(unittest.TestCase):
    """Test the State class"""

    def test_is_subclass_of_base_model(self):
        """Test that State is a subclass of BaseModel"""
        state = State()
        self.assertIsInstance(state, BaseModel)
        self.assertTrue(hasattr(state, "id"))
        self.assertTrue(hasattr(state, "created_at"))
        self.assertTrue(hasattr(state, "updated_at"))

    def test_attributes_initialization(self):
        """Test attributes initialization"""
        state = State()
        self.assertTrue(hasattr(state, "name"))
        if models.storage_t == 'db':
            self.assertIsNone(state.name)
        else:
            self.assertEqual(state.name, "")

    def test_to_dict_method(self):
        """Test to_dict method"""
        state = State()
        state_dict = state.to_dict()
        self.assertIsInstance(state_dict, dict)
        self.assertIn("__class__", state_dict)
        self.assertEqual(state_dict["__class__"], "State")
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)

    def test_to_dict_values(self):
        """Test values in dictionary returned from to_dict method"""
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertEqual(state_dict["created_at"], state.created_at.isoformat())
        self.assertEqual(state_dict["updated_at"], state.updated_at.isoformat())

    def test_string_representation(self):
        """Test the string representation of State instance"""
        state = State()
        string = "[State] ({}) {}".format(state.id, state.__dict__)
        self.assertEqual(string, str(state))


if __name__ == "__main__":
    unittest.main()

