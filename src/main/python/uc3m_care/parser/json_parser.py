"""Module for the AppointmentJsonParser module"""
import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonParser:
    """Class for the JsonParser object"""
    _JSON_KEYS = []
    _ERROR_MESSAGES = []
    FILE_NOT_FOUND_ERROR = "File is not found"
    WRONG_JSON_FORMAT_ERROR = "JSON Decode Error - Wrong JSON Format"

    def __init__(self, input_file):
        self._input_file = input_file
        self._json_content = self.load_json_content(input_file)
        self.validate_json_keys()

    def validate_json_keys(self):
        """Validates the keys inside the json file"""
        for key, error_message in zip(self._JSON_KEYS, self._ERROR_MESSAGES):
            if key not in self._json_content.keys():
                raise VaccineManagementException(error_message)

    def load_json_content(self, input_file):
        """Returns the contents of the json file"""
        # open the files
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.FILE_NOT_FOUND_ERROR) from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.WRONG_JSON_FORMAT_ERROR) from exception
        return data

    @property
    def json_content(self):
        """Property that represents the contents of the json file"""
        return self._json_content
