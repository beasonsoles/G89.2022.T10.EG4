from uc3m_care.data.attribute.attribute import Attribute


class DateSignature(Attribute):
    _validation_pattern = r"[0-9a-fA-F]{64}$"
    _validation_error_message = "date_signature format is not valid"
