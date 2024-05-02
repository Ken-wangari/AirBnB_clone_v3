#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""

import unittest
from datetime import datetime
from unittest.mock import patch
import inspect
import models.base_model as bm
import pep8

BaseModel = bm.BaseModel
module_doc = bm.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        paths = ['models/base_model.py', 'tests/test_models/test_base_model.py']
        for path in paths:
            with self.subTest(path=path):
                style = pep8.StyleGuide(quiet=True)
                result = style.check_files([path])
                self.assertEqual(result.total_errors, 0)

    def test_module_docstring(self):
        """Test for the existence and length of module docstring"""
        self.assertIsNotNone(module_doc)
        self.assertTrue(len(module_doc) > 1)

    def test_class_docstring(self):
        """Test for the existence and length of BaseModel class docstring"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertTrue(len(BaseModel.__doc__) >= 1)

    def test_func_docstrings(self):
        """Test for the presence and length of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNotNone(func[1].__doc__)
                self.assertTrue(len(func[1].__doc__) > 1)


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIsInstance(inst, BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertTrue(hasattr(inst, attr))
                self.assertIsInstance(getattr(inst, attr), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test that created_at and updated_at are datetime objects"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        self.assertIsInstance(inst1.created_at, datetime)
        self.assertIsInstance(inst1.updated_at, datetime)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid UUID"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            with self.subTest(inst=inst):
                self.assertIsInstance(inst.id, str)
                self.assertRegex(inst.id, bm.UUID_REGEX)
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for JSON"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "name", "my_number", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_str_representation(self):
        """Test the string representation of BaseModel"""
        inst = BaseModel()
        string = str(inst)
        expected = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, expected)

    @patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)


if __name__ == "__main__":
    unittest.main()

