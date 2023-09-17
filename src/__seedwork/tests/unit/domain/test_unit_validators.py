from dataclasses import fields
import unittest
from __seedwork.domain.exceptions import ValidationException

from __seedwork.domain.validators import ValidatorFieldsInterface, ValidatorRules


class TestValidatorRules(unittest.TestCase):
    def test_values_method(self):
        validator = ValidatorRules.values("value", "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "value")
        self.assertEqual(validator.prop, "prop")

    def test_rule_required(self):
        invalid_data = [{"value": None, "prop": "prop"},
                        {"value": "", "prop": "prop"}]

        for data in invalid_data:
            on_raise_msg = f"value: {data['value']}, prop: {data['prop']}"
            with self.assertRaises(ValidationException, msg=on_raise_msg) as assert_error:
                ValidatorRules.values(data["value"], data["prop"]).required()
            self.assertEqual("The field prop is required.",
                             assert_error.exception.args[0])

        valid_data = [{"value": "test", "prop": "prop"},
                      {"value": 5, "prop": "prop"},
                      {"value": 0, "prop": "prop"},
                      {"value": False, "prop": "prop"}]

        for data in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                data["value"], data["prop"]).required(), ValidatorRules)

    def test_rule_string(self):
        invalid_data = [{"value": 5, "prop": "prop"},
                        {"value": True, "prop": "prop"},
                        {"value": {}, "prop": "prop"}]

        for data in invalid_data:
            on_raise_msg = f"value: {data['value']}, prop: {data['prop']}"
            with self.assertRaises(ValidationException, msg=on_raise_msg) as assert_error:
                ValidatorRules.values(data["value"], data["prop"]).string()
            self.assertEqual(f"The field {data['prop']} must be a string.",
                             assert_error.exception.args[0])

        valid_data = [{"value": None, "prop": "prop"},
                      {"value": "", "prop": "prop"},
                      {"value": "some value", "prop": "prop"}]

        for data in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                data["value"], data["prop"]).string(), ValidatorRules)

    def test_rule_max_length(self):
        invalid_data = [{"value": "t" * 5, "prop": "prop"}]

        for data in invalid_data:
            on_raise_msg = f"value: {data['value']}, prop: {data['prop']}"
            with self.assertRaises(ValidationException, msg=on_raise_msg) as assert_error:
                max_len = 4
                ValidatorRules.values(
                    data["value"], data["prop"]).max_length(max_len)
            self.assertEqual(f"The field {data['prop']} cannot exceed {max_len} characters.",
                             assert_error.exception.args[0])

        valid_data = [{"value": "t" * 4, "prop": "prop"},
                      {"value": "t" * 1, "prop": "prop"},
                      {"value": "", "prop": "prop"}]

        for data in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                data["value"], data["prop"]).max_length(4), ValidatorRules)

    def test_rule_boolean(self):
        invalid_data = [{"value": "", "prop": "prop"},
                        {"value": 5, "prop": "prop"},
                        {"value": 5.0, "prop": "prop"},
                        {"value": {}, "prop": "prop"}]

        for data in invalid_data:
            on_raise_msg = f"value: {data['value']}, prop: {data['prop']}"
            with self.assertRaises(ValidationException, msg=on_raise_msg) as assert_error:
                ValidatorRules.values(
                    data["value"], data["prop"]).boolean()
            self.assertEqual(f"The field {data['prop']} must be a boolean.",
                             assert_error.exception.args[0])

        valid_data = [{"value": True, "prop": "prop"},
                      {"value": False, "prop": "prop"}]

        for data in valid_data:
            self.assertIsInstance(ValidatorRules.values(
                data["value"], data["prop"]).boolean(), ValidatorRules)

    def test_exception_when_combine_two_or_more_rules(self):
        max_len = 5
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None, "prop").required().string().max_length(max_len)
        self.assertEqual("The field prop is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5, "prop").required().string().max_length(max_len)
        self.assertEqual("The field prop must be a string.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                "a" * 6, "prop").required().string().max_length(max_len)
        self.assertEqual(f"The field prop cannot exceed {max_len} characters.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None, "prop").required().boolean()
        self.assertEqual("The field prop is required.",
                         assert_error.exception.args[0])

        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                "a", "prop").required().boolean()
        self.assertEqual("The field prop must be a boolean.",
                         assert_error.exception.args[0])

    def test_valid_combinations_between_rules(self):
        ValidatorRules("test", "prop").required().string()
        ValidatorRules("t" * 5, "prop").required().string().max_length(5)

        ValidatorRules(True, "prop").required().boolean()
        ValidatorRules(False, "prop").required().boolean()
        # pylint: disable=redundant-unittest-assert
        self.assertTrue(True)

class TestValidatorFieldsInterface(unittest.TestCase):

    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            ##pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            "Can't instantiate abstract class ValidatorFieldsInterface " + 
            "with abstract method validate", 
            assert_error.exception.args[0]
        )

    def test_validator_contract(self):
        fields_class = fields(ValidatorFieldsInterface)
        self._extracted_from_test_validator_fields(fields_class, 0, "errors")
        self._extracted_from_test_validator_fields(
            fields_class, 1, "validated_data"
        )

    def _extracted_from_test_validator_fields(self, fields_class, arg1, arg2):
        errors_field = fields_class[arg1]
        self.assertEqual(errors_field.name, arg2)
        self.assertIsNone(errors_field.default)
