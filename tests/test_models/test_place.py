#!/usr/bin/python3
"""
Contains TestPlaceDocs and TestPlace classes
"""

from datetime import datetime
import inspect
import models
from models.place import Place
from models.base_model import BaseModel
import pep8
import unittest


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_place.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertIsNot(models.place.__doc__, None,
                         "place.py needs a docstring")
        self.assertTrue(len(models.place.__doc__) >= 1,
                        "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNot(Place.__doc__, None,
                         "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertIsNot(func[1].__doc__, None,
                             f"{func[0]} method needs a docstring")
            self.assertTrue(len(func[1].__doc__) >= 1,
                            f"{func[0]} method needs a docstring")


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def setUp(self):
        """Set up instances for testing"""
        self.place = Place()

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        self.assertIsInstance(self.place, BaseModel)
        self.assertTrue(hasattr(self.place, "id"))
        self.assertTrue(hasattr(self.place, "created_at"))
        self.assertTrue(hasattr(self.place, "updated_at"))

    def test_attributes(self):
        """Test Place attributes"""
        attrs_types = {
            "city_id": str,
            "user_id": str,
            "name": str,
            "description": str,
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(self.place, attr))
                self.assertIsInstance(getattr(self.place, attr), typ)
                if typ == int:
                    self.assertEqual(getattr(self.place, attr), 0)
                elif typ == float:
                    self.assertEqual(getattr(self.place, attr), 0.0)
                else:
                    self.assertEqual(getattr(self.place, attr), "")

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_place = self.place
        my_place.name = "Holberton"
        my_place.my_number = 89
        d = my_place.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'Place')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_str(self):
        """Test that the str method has the correct output"""
        string = "[Place] ({}) {}".format(self.place.id, self.place.__dict__)
        self.assertEqual(string, str(self.place))

