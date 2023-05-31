import unittest
from datetime import datetime
from dataclasses import is_dataclass, FrozenInstanceError
from category.domain.entities import Category


class TestCategoryUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        def _assert_test_constructor(category, arg1, arg2, arg3):
            self.assertEqual(category.name, "Movie")
            self.assertEqual(category.description, arg1)
            self.assertEqual(category.is_active, arg2)
            self.assertIsInstance(category.created_at, arg3)

        data = {
            "name": "Movie",
            "description": "description",
            "is_active": False,
            "created_at": datetime.now(),
        }

        category = Category(name=data["name"])
        category2 = Category(**data)

        _assert_test_constructor(category, None, True, datetime)
        _assert_test_constructor(category2, "description", False, datetime)

    def test_if_created_at_are_different_between_two_instances(self):
        category1 = Category(name="Movie 1")
        category2 = Category(name="Movie 2")
        self.assertNotEqual(category1.created_at, category2.created_at)

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = Category(name="test name")
            value_object.name = "fake name"

    def test_update_name_and_description(self):
        category = Category(name="Movie 1", description="nice movie")
        category.update("Movie 2", "bad movie")
        self.assertEqual(category.name, "Movie 2")
        self.assertEqual(category.description, "bad movie")

    def test_activate(self):
        category = Category(name="Movie 1", is_active=False)
        category.activate()
        self.assertTrue(category.is_active)

    def test_deactivate(self):
        category = Category(name="Movie 1")
        category.deactivate()
        self.assertFalse(category.is_active)
