#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest

# Alias for better readability
Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_methods = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test PEP8 conformance of place.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/place.py'])
        self.assertEqual(
            result.total_errors, 0,
            "PEP8 style errors and warnings found in place.py"
        )

    def test_pep8_conformance_test_place(self):
        """Test PEP8 conformance of test_place.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(
            result.total_errors, 0,
            "PEP8 style errors and warnings found in test_place.py"
        )

    def test_place_module_docstring(self):
        """Test if place.py module has a docstring"""
        self.assertIsNotNone(place.__doc__, "place.py needs a docstring")
        self.assertTrue(len(place.__doc__) >= 1, "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test if Place class has a docstring"""
        self.assertIsNotNone(Place.__doc__, "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1, "Place class needs a docstring")

    def test_place_method_docstrings(self):
        """Test if Place class methods have docstrings"""
        for method_name, method_obj in self.place_methods:
            with self.subTest(method_name=method_name):
                self.assertIsNotNone(
                    method_obj.__doc__,
                    f"{method_name} method needs a docstring"
                )
                self.assertTrue(
                    len(method_obj.__doc__) >= 1,
                    f"{method_name} method needs a docstring"
                )


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def test_is_subclass(self):
        """Test if Place is a subclass of BaseModel"""
        place_instance = Place()
        self.assertIsInstance(place_instance, BaseModel)
        self.assertTrue(hasattr(place_instance, "id"))
        self.assertTrue(hasattr(place_instance, "created_at"))
        self.assertTrue(hasattr(place_instance, "updated_at"))

    def test_attributes_default_values(self):
        """Test default values of Place attributes"""
        place_instance = Place()
        attributes = ["city_id", "user_id", "name", "description",
                      "number_rooms", "number_bathrooms", "max_guest",
                      "price_by_night", "latitude", "longitude"]
        for attr in attributes:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(place_instance, attr))
                if models.storage_t == 'db':
                    self.assertIsNone(getattr(place_instance, attr))
                else:
                    self.assertEqual(getattr(place_instance, attr), "")

    @unittest.skipIf(models.storage_t == 'db', "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Test Place amenity_ids attribute"""
        place_instance = Place()
        self.assertTrue(hasattr(place_instance, "amenity_ids"))
        self.assertEqual(type(place_instance.amenity_ids), list)
        self.assertEqual(len(place_instance.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """Test if to_dict method creates a dictionary with proper attrs"""
        place_instance = Place()
        new_dict = place_instance.to_dict()
        self.assertEqual(type(new_dict), dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr in place_instance.__dict__:
            with self.subTest(attr=attr):
                if attr != "_sa_instance_state":
                    self.assertIn(attr, new_dict)
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test if values in dictionary returned from to_dict are correct"""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        place_instance = Place()
        new_dict = place_instance.to_dict()
        self.assertEqual(new_dict["__class__"], "Place")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(
            new_dict["created_at"], place_instance.created_at.strftime(time_format)
        )
        self.assertEqual(
            new_dict["updated_at"], place_instance.updated_at.strftime(time_format)
        )

    def test_str(self):
        """Test if the str method has the correct output"""
        place_instance = Place()
        string = "[Place] ({}) {}".format(place_instance.id, place_instance.__dict__)
        self.assertEqual(string, str(place_instance))


if __name__ == "__main__":
    unittest.main()

