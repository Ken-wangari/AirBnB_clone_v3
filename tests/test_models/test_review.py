#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

import unittest
import pep8
import inspect
from models.review import Review
from models.base_model import BaseModel
import models


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_funcs = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review_module(self):
        """Test that models/review.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in review module")

    def test_pep8_conformance_test_review_module(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found in test_review module")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNotNone(Review.__doc__, "review.py needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1, "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNotNone(Review.__doc__, "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1, "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for func_name, func in self.review_funcs:
            with self.subTest(function=func_name):
                self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1, f"{func_name} method needs a docstring")


class TestReview(unittest.TestCase):
    """Test the Review class"""

    def test_is_subclass_of_base_model(self):
        """Test if Review is a subclass of BaseModel"""
        review = Review()
        self.assertIsInstance(review, BaseModel)
        self.assertTrue(hasattr(review, "id"))
        self.assertTrue(hasattr(review, "created_at"))
        self.assertTrue(hasattr(review, "updated_at"))

    def test_attributes_initialization(self):
        """Test attributes initialization"""
        attributes = ["place_id", "user_id", "text"]
        review = Review()
        for attr in attributes:
            self.assertTrue(hasattr(review, attr))
            if models.storage_t == 'db':
                self.assertIsNone(getattr(review, attr))
            else:
                self.assertEqual(getattr(review, attr), "")

    def test_to_dict_method(self):
        """Test to_dict method"""
        review = Review()
        review_dict = review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertFalse("_sa_instance_state" in review_dict)
        for attr in review.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in review_dict)
        self.assertTrue("__class__" in review_dict)

    def test_to_dict_values(self):
        """Test values in dictionary returned from to_dict method"""
        review = Review()
        review_dict = review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertEqual(review_dict["created_at"], review.created_at.isoformat())
        self.assertEqual(review_dict["updated_at"], review.updated_at.isoformat())

    def test_string_representation(self):
        """Test the string representation of Review instance"""
        review = Review()
        string = "[Review] ({}) {}".format(review.id, review.__dict__)
        self.assertEqual(string, str(review))


if __name__ == "__main__":
    unittest.main()

