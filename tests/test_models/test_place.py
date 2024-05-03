#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

import unittest
import pep8
import inspect
from models.place import Place
from models.base_model import BaseModel
import models


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_funcs = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place_module(self):
        """Test that models/place.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in place module")

    def test_pep8_conformance_test_place_module(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in test_place module")

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertIsNotNone(Place.__doc__, "place.py needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1, "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNotNone(Place.__doc__, "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1, "Place class needs a docstring")

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func_name, func in self.place_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def test_is_subclass_of_base_model(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_attributes_initialization(self):
        """Test attributes initialization"""
        attributes = ["city_id", "user_id", "name", "description", "number_rooms",
                      "number_bathrooms", "max_guest", "price_by_night", "latitude", "longitude"]
        place = Place()
        for attr in attributes:
            self.assertTrue(hasattr(place, attr))
            if models.storage_t == 'db':
                self.assertIsNone(getattr(place, attr))
            else:
                self.assertEqual(getattr(place, attr), "")

    def test_amenity_ids_attr(self):
        """Test amenity_ids attribute"""
        place = Place()
        if models.storage_t == 'db':
            self.assertIsNone(place.amenity_ids)
        else:
            self.assertIsInstance(place.amenity_ids, list)
            self.assertEqual(len(place.amenity_ids), 0)

    def test_to_dict_method(self):
        """Test to_dict method"""
        place = Place()
        place_dict = place.to_dict()
        self.assertIsInstance(place_dict, dict)
        self.assertFalse("_sa_instance_state" in place_dict)
        for attr in place.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in place_dict)
        self.assertTrue("__class__" in place_dict)

    def test_to_dict_values(self):
        """Test values in dictionary returned from to_dict method"""
        place = Place()
        place_dict = place.to_dict()
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertEqual(place_dict["created_at"], place.created_at.isoformat())
        self.assertEqual(place_dict["updated_at"], place.updated_at.isoformat())

    def test_string_representation(self):
        """Test the string representation of Place instance"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))


if __name__ == "__main__":
    unittest.main()

