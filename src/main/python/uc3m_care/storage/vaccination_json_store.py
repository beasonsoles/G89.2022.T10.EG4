from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class VaccinationJsonStore(JsonStore):
    class __VaccinationJsonStore(JsonStore):
        _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"
        _ID_FIELD = "_VaccinationLog__date_signature"

        def add_item(self, item):
            from uc3m_care.data.vaccination_log import VaccinationLog
            if not isinstance(item, VaccinationLog):
                raise VaccineManagementException("Invalid VaccinationLog object")
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
