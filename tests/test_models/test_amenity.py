#!/usr/bin/python3
"""
Contains the TestAmenityDocs classes
"""

import unittest
import pep8
from models.amenity import Amenity
from datetime import datetime
import inspect

class TestAmenityDocs(unittest.TestCase):
    """Tests to check the documentation and style of Amenity class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.amenity_f = inspect.getmembers(Amenity, inspect.isfunction)

    def test_pep8_conformance_amenity(self):
        """Test that models/amenity.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_amenity(self):
        """Test that tests/test_models/test_amenity.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_amenity_module_docstring(self):
        """Test for the amenity.py module docstring"""
        self.assertIsNot(Amenity.__doc__, None,
                         "amenity.py needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "amenity.py needs a docstring")

    def test_amenity_class_docstring(self):
        """Test for the Amenity class docstring"""
        self.assertIsNot(Amenity.__doc__, None,
                         "Amenity class needs a docstring")
        self.assertTrue(len(Amenity.__doc__) >= 1,
                        "Amenity class needs a docstring")

    def test_amenity_func_docstrings(self):
        """Test for the presence of docstrings in Amenity methods"""
        for func in self.amenity_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestAmenity(unittest.TestCase):
    """Test the Amenity class"""

    def setUp(self):
        """Set up for testing"""
        self.amenity = Amenity()

    def tearDown(self):
        """Clean up after each test method"""
        del self.amenity

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel"""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_attributes(self):
        """Test that Amenity instance attributes exist"""
        self.assertTrue(hasattr(self.amenity, "id"))
        self.assertTrue(hasattr(self.amenity, "created_at"))
        self.assertTrue(hasattr(self.amenity, "updated_at"))

    def test_name_attr(self):
        """Test that Amenity has attribute name, and it's an empty string"""
        self.assertTrue(hasattr(self.amenity, "name"))
        if models.storage_t == 'db':
            self.assertIsNone(self.amenity.name)
        else:
            self.assertEqual(self.amenity.name, "")

    def test_to_dict_creates_dict(self):
        """Test that to_dict method creates a dictionary with proper attrs"""
        new_dict = self.amenity.to_dict()
        self.assertIsInstance(new_dict, dict)
        self.assertFalse("_sa_instance_state" in new_dict)
        for attr in self.amenity.__dict__:
            if attr is not "_sa_instance_state":
                self.assertIn(attr, new_dict)
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_dict = self.amenity.to_dict()
        self.assertEqual(new_dict["__class__"], "Amenity")
        self.assertIsInstance(new_dict["created_at"], str)
        self.assertIsInstance(new_dict["updated_at"], str)
        self.assertEqual(new_dict["created_at"], self.amenity.created_at.strftime(t_format))
        self.assertEqual(new_dict["updated_at"], self.amenity.updated_at.strftime(t_format))

    def test_str_representation(self):
        """Test that the str method has the correct output"""
        string = str(self.amenity)
        self.assertEqual(string, "[Amenity] ({}) {}".format(self.amenity.id, self.amenity.__dict__))

