import json
from uc3m_care.vaccine_management_exception import VaccineManagementException


class JsonStore:
    _FILE_PATH = ""
    _ID_FIELD = ""

    def __init__(self):
        pass

    def load(self):
        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            data_list = []
        return data_list

    def save(self, data_list):
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    def add_item(self, item):
        data_list = self.load()
        data_list.append(item.__dict__)
        self.save(data_list)

    def find_item(self, key_value, key=None):
        data_list = self.load()
        if key is None:
            key = self._ID_FIELD
        for item in data_list:
            if item[key] == key_value:
                return item
        return None

    def find_item_list(self, key_value, key=None):
        data_list = self.load()
        if key is None:
            key = self._ID_FIELD
        data_list_result = []
        for item in data_list:
            if item[key] == key_value:
                data_list_result.append(item)
        return data_list_result
