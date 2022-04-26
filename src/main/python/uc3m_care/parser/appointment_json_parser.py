from .json_parser import JsonParser


class AppointmentJsonParser(JsonParser):
    _JSON_KEYS = ["PatientSystemID", "ContactPhoneNumber"]
    _ERROR_MESSAGES = ["Bad label patient_id", "Bad label contact phone"]
