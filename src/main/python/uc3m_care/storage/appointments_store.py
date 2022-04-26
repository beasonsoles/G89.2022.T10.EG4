from uc3m_care.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class AppointmentsStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + 'store_date.json'
    _ID_FIELD = 'VaccinationAppointment__date_signature'

    def add_item(self, item):
        from uc3m_care.data.vaccination_appoinment import VaccinationAppoinment
        if not isinstance(item, VaccinationAppoinment):
            raise VaccineManagementException("Invalid appointment object")
        super().add_item(item)
