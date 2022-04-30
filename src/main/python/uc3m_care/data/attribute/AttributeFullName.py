"""Module for the attribute FullName"""
from .Attribute import Attribute

class FullName(Attribute):
    """Attribute class for FullName"""
    _validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    _validation_error_message = "name surname is not valid"
