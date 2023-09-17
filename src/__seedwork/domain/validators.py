import abc
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from rest_framework.serializers import Serializer

from .exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules():
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> 'ValidatorRules':
        if self.value is not None and self.value == "" or self.value is None:
            raise ValidationException(F"The field {self.prop} is required.")
        return self

    def string(self) -> 'ValidatorRules':
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(
                f"The field {self.prop} must be a string.")
        return self

    def max_length(self, max_len: int) -> 'ValidatorRules':
        if self.value is not None and len(self.value) > max_len:
            raise ValidationException(
                f"The field {self.prop} cannot exceed {max_len} characters.")
        return self

    def boolean(self) -> 'ValidatorRules':
        if self.value is not None and self.value is not True and self.value is not False:
            raise ValidationException(
                f"The field {self.prop} must be a boolean.")
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar("PropsValidated")


@dataclass(slots=True)
class ValidatorFieldsInterface(abc.ABC, Generic[PropsValidated]):
    errors: ErrorFields = None
    validated_data: PropsValidated = None

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated]):
    def validate(self, data: Serializer):
        if not data.is_valid():
            self.errors = {
                field: [str(_error) for _error in _errors]
                for field, _errors in data.errors.item()
            }
        else:
            self.validated_data = data.validated_data
            return True
