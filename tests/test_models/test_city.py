#!/usr/bin/python3
"""
Contains TestCityDocs and TestCity classes
"""

import unittest
import pep8
from datetime import datetime
import inspect
from models.city import City
from models.base_model import BaseModel


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.city_funcs = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance_city_module(self):
        """Test that models/city.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in city module")

    def test_pep8_conformance_test_city_module(self):
        """Test that tests/test_models/test_city.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_city.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in test_city module")

    def test_city_module_docstring(self):
        """Test for the city.py module docstring"""
        self.assertIsNotNone(City.__doc__, "city.py needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1, "city.py needs a docstring")

    def test_city_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNotNone(City.__doc__, "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1, "City class needs a docstring")

    def test_city_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func_name, func in self.city_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestCity(unittest.TestCase):
    """Test the City class"""

    def test_is_subclass_of_base_model(self):
        """Test that City is a subclass of BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)
        self.assertTrue(hasattr(city, "id"))
        self.assertTrue(hasattr(city, "created_at"))
        self.assertTrue(hasattr(city, "updated_at"))

    def test_name_attribute(self):
        """Test that City has 'name' attribute, initialized to empty string or None"""
        city = City()
        self.assertTrue(hasattr(city, "name"))
        self.assertTrue(city.name == "" or city.name is None)

    def test_state_id_attribute(self):
        """Test that City has 'state_id' attribute, initialized to empty string or None"""
        city = City()
        self.assertTrue(hasattr(city, "state_id"))
        self.assertTrue(city.state_id == "" or city.state_id is None)

    def test_to_dict_method(self):
        """Test that to_dict method returns dictionary with correct attributes and values"""
        city = City()
        city_dict = city.to_dict()
        self.assertIsInstance(city_dict, dict)
        self.assertTrue(all(attr in city_dict for attr in city.__dict__))
        self.assertTrue("__class__" in city_dict)
        self.assertTrue("created_at" in city_dict)
        self.assertTrue("updated_at" in city_dict)
        self.assertEqual(city_dict["__class__"], "City")

    def test_to_dict_values(self):
        """Test that values in dictionary returned from to_dict method are correct"""
        city = City()
        city_dict = city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertEqual(city_dict["created_at"], city.created_at.isoformat())
        self.assertEqual(city_dict["updated_at"], city.updated_at.isoformat())

    def test_string_representation(self):
        """Test the string representation of City instance"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))


if __name__ == "__main__":
    unittest.main()

