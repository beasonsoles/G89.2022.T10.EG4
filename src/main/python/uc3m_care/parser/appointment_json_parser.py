"""Module for the AppointmentJsonParser module"""
from uc3m_care.parser.json_parser import JsonParser


class AppointmentJsonParser(JsonParser):
    """Class containing the attributes for the AppointmentJsonParser object"""
    # magic strings
    PATIENT_SYSTEM_ID_KEY = "PatientSystemID"
    CONTACT_PHONE_NUMBER_KEY = "ContactPhoneNumber"
    BAD_PHONE_NUMBER_LABEL_ERROR = "Bad label contact phone"
    BAD_PATIENT_SYS_ID_LABEL_ERROR = "Bad label patient_id"
    _JSON_KEYS = [PATIENT_SYSTEM_ID_KEY, CONTACT_PHONE_NUMBER_KEY]
    _ERROR_MESSAGES = [BAD_PATIENT_SYS_ID_LABEL_ERROR, BAD_PHONE_NUMBER_LABEL_ERROR]
