#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""

import unittest
import pep8
from datetime import datetime
from unittest.mock import patch
from models.base_model import BaseModel


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = [func for func in dir(BaseModel) if callable(getattr(BaseModel, func))]

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/base_model.py', 'tests/test_models/test_base_model.py'])
        self.assertEqual(result.total_errors, 0, "PEP8 style violations found")

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNotNone(BaseModel.__doc__, "base_model.py needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) > 1, "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNotNone(BaseModel.__doc__, "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func_name in self.base_funcs:
            func = getattr(BaseModel, func_name)
            self.assertIsNotNone(func.__doc__, f"{func_name} method needs a docstring")
            self.assertTrue(len(func.__doc__) > 1, f"{func_name} method needs a docstring")


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIsInstance(inst, BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test datetime attributes"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertNotEqual(inst1.id, inst2.id)
        self.assertIsInstance(inst1.created_at, datetime)
        self.assertIsInstance(inst1.updated_at, datetime)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test to_dict method"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_str(self):
        """Test str method"""
        inst = BaseModel()
        self.assertIn('BaseModel', str(inst))
        self.assertIn(inst.id, str(inst))

    @patch('models.storage')
    def test_save(self, mock_storage):
        """Test save method"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        mock_storage.save.assert_called_once()

