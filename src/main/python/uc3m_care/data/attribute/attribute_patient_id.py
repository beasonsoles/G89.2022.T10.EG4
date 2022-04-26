"""Module for the attribute PatientID"""
import uuid
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from .attribute import Attribute


class PatientID(Attribute):
    """Attribute class for PatientID"""
    _validation_pattern = r"^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab]" \
                          r"[0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$"
    _validation_error_message = "UUID invalid"

    def _validate(self, attr_value):
        try:
            patient_uuid = uuid.UUID(attr_value)
        except ValueError as val_er:
            raise VaccineManagementException("Id received is not a UUID") from val_er
        return super()._validate(attr_value)