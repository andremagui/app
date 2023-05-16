import unittest
from datetime import datetime
from category.domain.entities import Category
from dataclasses import is_dataclass


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        def _assert_test_constructor(category, arg1, arg2, arg3):
            # Assert
            self.assertEqual(category.name, "Movie")
            self.assertEqual(category.description, arg1)
            self.assertEqual(category.is_active, arg2)
            self.assertIsInstance(category.created_at, arg3)

        # Triple AAA

        # Arrange
        data = {
            "name": "Movie",
            "description": "description",
            "is_active": False,
            "created_at": datetime.now(),
        }

        # Act
        category = Category(data["name"])
        category2 = Category(**data)

        # Assert
        _assert_test_constructor(category, None, True, datetime)
        _assert_test_constructor(category2, "description", False, datetime)

    def test_if_created_at_are_different_between_two_instances(self):
        category1 = Category(name="Movie 1")
        category2 = Category(name="Movie 2")
        self.assertNotEqual(category1.created_at, category2.created_at)
        # self.assertNotEqual(
        #    category1.created_at.timestamp(), category2.created_at.timestamp()
        # )
