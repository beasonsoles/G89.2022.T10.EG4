"""Module for the attribute RegistrationType"""
from .Attribute import Attribute


class RegistrationType(Attribute):
    """Attribute class for RegistrationType"""
    _validation_pattern = r"(Regular|Family)"
    _validation_error_message = "Registration type is not valid"
