"""Module for the attribute PhoneNumber"""
from .attribute import Attribute


class PhoneNumber(Attribute):
    """Attribute class for PhoneNumber"""
    _validation_pattern = r"^(\+)[0-9]{11}"
    _validation_error_message = "phone number is not valid"
