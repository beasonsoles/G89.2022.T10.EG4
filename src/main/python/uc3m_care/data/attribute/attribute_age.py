"""Module for the attribute Age"""
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.attribute.attribute import Attribute


class Age(Attribute):
    """Attribute class for Age"""
    _validation_error_message = "age is not valid"

    def _validate(self, attr_value):
        if attr_value.isnumeric():
            if int(attr_value) < 6 or int(attr_value) > 125:
                raise VaccineManagementException(self._validation_error_message)
        else:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
