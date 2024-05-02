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

Review = review.Review


class TestReviewDocs(unittest.TestCase):
    """Tests to check the documentation and style of Review class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.review_f = inspect.getmembers(Review, inspect.isfunction)

    def test_pep8_conformance_review(self):
        """Test that models/review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_review(self):
        """Test that tests/test_models/test_review.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_review.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_review_module_docstring(self):
        """Test for the review.py module docstring"""
        self.assertIsNot(review.__doc__, None,
                         "review.py needs a docstring")
        self.assertTrue(len(review.__doc__) >= 1,
                        "review.py needs a docstring")

    def test_review_class_docstring(self):
        """Test for the Review class docstring"""
        self.assertIsNot(Review.__doc__, None,
                         "Review class needs a docstring")
        self.assertTrue(len(Review.__doc__) >= 1,
                        "Review class needs a docstring")

    def test_review_func_docstrings(self):
        """Test for the presence of docstrings in Review methods"""
        for name, func in self.review_f:
            with self.subTest(name=name):
                self.assertIsNotNone(func.__doc__,
                                     f"{name} method needs a docstring")
                self.assertTrue(len(func.__doc__) >= 1,
                                f"{name} method needs a docstring")


class TestReview(unittest.TestCase):
    """Test the Review class"""

    def setUp(self):
        """Set up an instance of Review for testing"""
        self.review = Review()

    def test_is_subclass(self):
        """Test if Review is a subclass of BaseModel"""
        self.assertIsInstance(self.review, BaseModel)
        self.assertTrue(hasattr(self.review, "id"))
        self.assertTrue(hasattr(self.review, "created_at"))
        self.assertTrue(hasattr(self.review, "updated_at"))

    def test_place_id_attr(self):
        """Test Review has attr place_id, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertEqual(self.review.place_id, "")

    def test_user_id_attr(self):
        """Test Review has attr user_id, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertEqual(self.review.user_id, "")

    def test_text_attr(self):
        """Test Review has attr text, and it's an empty string"""
        self.assertTrue(hasattr(self.review, "text"))
        self.assertEqual(self.review.text, "")

    def test_to_dict_creates_dict(self):
        """Test to_dict method creates a dictionary with proper attrs"""
        new_d = self.review.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in self.review.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        new_d = self.review.to_dict()
        self.assertEqual(new_d["__class__"], "Review")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"],
                         self.review.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"],
                         self.review.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        string = "[Review] ({}) {}".format(self.review.id, self.review.__dict__)
        self.assertEqual(string, str(self.review))

