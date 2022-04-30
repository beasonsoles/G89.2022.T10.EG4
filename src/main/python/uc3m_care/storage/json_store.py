"""Module for the JsonStore class"""
import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class JsonStore:
    """Class for managing the json files"""
    _FILE_PATH = ""
    _ID_FIELD = ""
    PATIENT_ID = "_VaccinePatientRegister__patient_id"
    REGISTRATION_TYPE = "_VaccinePatientRegister__registration_type"
    FULL_NAME = "_VaccinePatientRegister__full_name"
    REGISTER_PHONE_NUMBER = "_VaccinePatientRegister__phone_number"
    AGE = "_VaccinePatientRegister__age"
    TIME_STAMP = "_VaccinePatientRegister__time_stamp"
    PATIENT_SYSTEM_ID = "_VaccinationAppointment__patient_sys_id"
    APPOINTMENT_PHONE_NUMBER = "_VaccinationAppointment__phone_number"
    ISSUED_DATE = "_VaccinationAppointment__issued_at"
    ERROR_JSON_FORMAT = "JSON Decode Error - Wrong JSON Format"
    ERROR_FILE_NOT_FOUND = "Wrong file or file path"

    def __init__(self):
        pass

    def load(self):
        """Method that returns the contents of the file"""
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException(self.ERROR_JSON_FORMAT) from exception
        except FileNotFoundError:
            data_list = []
        return data_list

    def save(self, data_list):
        """Method that saves data into the file"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException(self.ERROR_FILE_NOT_FOUND) from exception

    def add_item(self, item):
        """Method that inserts an item into the data of the file"""
        data_list = self.load()
        data_list.append(item.__dict__)
        self.save(data_list)

    def find_item(self, key_value, key=None):
        """Method that finds an item given the value of one of its keys"""
        data_list = self.load()
        if key is None:
            key = self._ID_FIELD
        for item in data_list:
            if item[key] == key_value:
                return item
        return None

    def find_item_list(self, key_value, key=None):
        """Method that returns the items that match the given key"""
        data_list = self.load()
        if key is None:
            key = self._ID_FIELD
        data_list_result = []
        for item in data_list:
            if item[key] == key_value:
                data_list_result.append(item)
        return data_list_result
