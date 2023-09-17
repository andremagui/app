import unittest
from __seedwork.domain.exceptions import ValidationException

from category.domain.entities import Category

#pylint: disable=trailing-whitespace
class TestCategoryIntegration(unittest.TestCase):
    def test_create_with_invalid_cases_for_name_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name=None)
        self.assertEqual("The field name is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            Category(name="")
        self.assertEqual("The field name is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            Category(name=5)
        self.assertEqual("The field name must be a string.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            Category(name="t" * 256)
        self.assertEqual("The field name cannot exceed 255 characters.",
                         assert_error.exception.args[0])
        
    def test_create_with_invalid_cases_for_description_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name="Movie", description=5)
        self.assertEqual("The field description must be a string.",
                         assert_error.exception.args[0])
        
    def test_create_with_invalid_cases_for_is_active_prop(self):
        with self.assertRaises(ValidationException) as assert_error:
            Category(name="Movie", is_active=5)
        self.assertEqual("The field is_active must be a boolean.",
                         assert_error.exception.args[0])
        
    def test_create_with_valid_cases(self):
        try:
            Category(name="Movie")
            Category(name="Movie", description="Nice movie")
            Category(name="Movie", description="")
            Category(name="Movie", description=None)
            Category(name="Movie", description="Nice movie", is_active=False)
            Category(name="Movie", is_active=True)
            Category(name="Movie", is_active=False)
        except ValidationException as err:
            self.fail(f"Some prop is not valid. Error: {err.args[0]}")

    def test_update_with_invalid_cases_for_name_prop(self):
        category = Category(name="Movie")
        with self.assertRaises(ValidationException) as assert_error:
            category.update(None, None) #NOSONAR
        self.assertEqual("The field name is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            category.update("", "")
        self.assertEqual("The field name is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            category.update(5, "")
        self.assertEqual("The field name must be a string.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            category.update("t" * 256, "")
        self.assertEqual("The field name cannot exceed 255 characters.",
                         assert_error.exception.args[0])
              
    def test_update_with_invalid_cases_for_description_prop(self):
        category = Category(name="Movie", description="Nice movie")
        with self.assertRaises(ValidationException) as assert_error:
            category.update(name="Movie", description=5)
        self.assertEqual("The field description must be a string.",
                         assert_error.exception.args[0])
        
    def test_update_with_valid_cases(self):
        new_name = "Movie 2"
        category = Category(name="Movie")
        try:
            category.update(name=new_name, description=None)
            category.update(name=new_name, description="")
            category.update(name=new_name, description="Nice movie")
        except ValidationException as err:
            self.fail(f"Some prop is not valid. Error: {err.args[0]}")
            