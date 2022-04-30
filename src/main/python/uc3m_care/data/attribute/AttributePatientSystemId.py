"""Module for the attribute PatientSystemID"""
from .Attribute import Attribute


class PatientSystemID(Attribute):
    """Attribute class for PatientSystemID"""
    _validation_pattern = r"[0-9a-fA-F]{32}$"
    _validation_error_message = "patient system id is not valid"
