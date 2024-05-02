#!/usr/bin/python3
"""
Contains the TestReviewDocs classes
"""

from datetime import datetime
import inspect
import models
from models import review
from models.base_model import BaseModel
import pep8
import unittest

# Alias for better readability
Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_methods = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test PEP8 conformance of review.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/review.py'])
        self.assertEqual(
            result.total_errors, 0,
            "PEP8 style errors and warnings found in review.py"
        )

    def test_pep8_conformance_test_review(self):
        """Test PEP8 conformance of test_review.py"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(
            result.total_errors, 0,
            "PEP8 style errors and warnings found in test_review.py"
        )

    def test_review_module_docstring(self):
        """Test if review.py module has a docstring"""
        self.assertIsNotNone(review.__doc__, "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1, "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test if Review class has a docstring"""
        self.assertIsNotNone(Review.__doc__, "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1, "Review class needs a docstring")

    def test_review_method_docstrings(self):
        """Test if Review class methods have docstrings"""
        for method_name, method_obj in self.review_methods:
            with self.subTest(method_name=method_name):
                self.assertIsNotNone(
                    method_obj.__doc__,
                    f"{method_name} method needs a docstring"
                )
                self.assertTrue(
                    len(method_obj.__doc__) >= 1,
                    f"{method_name} method needs a docstring"
                )


class TestReview(unittest.TestCase):
    """Test the Review class"""

    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        review_instance = Review()
        self.assertIsInstance(review_instance, BaseModel)
        self.assertTrue(hasattr(review_instance, "id"))
        self.assertTrue(hasattr(review_instance, "created_at"))
        self.assertTrue(hasattr(review_instance, "updated_at"))

    def test_attributes_default_values(self):
        """Test default values of Review attributes"""
        review_instance = Review()
        attributes = ["place_id", "user_id", "text"]
        for attr in attributes:
            with self.subTest(attr=attr):
                self.assertTrue(hasattr(review_instance, attr))
                if models.storage_t == 'db':
                    self.assertIsNone(getattr(review_instance, attr))
                else:
                    self.assertEqual(getattr(review_instance, attr), "")

    def test_to_dict_creates_dict(self):
        """Test if to_dict method creates a dictionary with proper attrs"""
        review_instance = Review()
        new_dict = review_instance.to_dict()
        self.assertEqual(type(new_dict), dict)
        self.assertNotIn("_sa_instance_state", new_dict)
        for attr in review_instance.__dict__:
            with self.subTest(attr=attr):
                if attr != "_sa_instance_state":
                    self.assertIn(attr, new_dict)
        self.assertIn("__class__", new_dict)

    def test_to_dict_values(self):
        """Test if values in dictionary returned from to_dict are correct"""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        review_instance = Review()
        new_dict = review_instance.to_dict()
        self.assertEqual(new_dict["__class__"], "Review")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(
            new_dict["created_at"], review_instance.created_at.strftime(time_format)
        )
        self.assertEqual(
            new_dict["updated_at"], review_instance.updated_at.strftime(time_format)
        )

    def test_str(self):
        """Test if the str method has the correct output"""
        review_instance = Review()
        string = "[Review] ({}) {}".format(review_instance.id, review_instance.__dict__)
        self.assertEqual(string, str(review_instance))


if __name__ == "__main__":
    unittest.main()

