from uc3m_care.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class VaccinationJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_vaccine.json"
    _ID_FIELD = "_VaccinationLog__date_signature"

    def add_item(self, item):
        from uc3m_care.data.vaccination_log import VaccinationLog
        if not isinstance(item, VaccinationLog):
            raise VaccineManagementException("Invalid VaccinationLog object")
        super().add_item(item)
