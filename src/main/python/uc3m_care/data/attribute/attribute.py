"""Module for the attribute class pattern"""
import re
from uc3m_care.vaccine_management_exception import VaccineManagementException


class Attribute():
    """Attribute pattern class"""
    _validation_pattern = r""
    _validation_error_message = ""
    _Value = ""

    def __init__(self, attr_value):
        self._value = self._validate(attr_value)

    @property
    def value(self):
        """Returns the value"""
        return self._value

    @value.setter
    def value(self, attr_value):
        self._value = self._validate(attr_value)

    def _validate(self, attr_value):
        pattern = re.compile(self._validation_pattern)
        result = pattern.fullmatch(attr_value)
        if not result:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
