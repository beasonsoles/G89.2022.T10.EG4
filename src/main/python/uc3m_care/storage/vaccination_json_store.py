"""Module for the VaccinationJsonStore object"""
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class VaccinationJsonStore(JsonStore):
    """Class for the management of the json file for the vaccinations"""
    class __VaccinationJsonStore(JsonStore):
        """Private Class for applying the Singleton Pattern"""
        _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"
        _ID_FIELD = "_VaccinationLog__date_signature"
        INVALID_VACCINELOG_OBJECT_ERROR = "Invalid VaccinationLog object"

        def add_item(self, item):
            from uc3m_care.data.vaccination_log import VaccinationLog
            if not isinstance(item, VaccinationLog):
                raise VaccineManagementException(self.INVALID_VACCINELOG_OBJECT_ERROR)
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not VaccinationJsonStore.instance:
            VaccinationJsonStore.instance = VaccinationJsonStore.__VaccinationJsonStore()

        return VaccinationJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
