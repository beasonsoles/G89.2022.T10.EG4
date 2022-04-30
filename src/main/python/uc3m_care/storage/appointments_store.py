"""Module for the AppointmentsStore object"""
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class AppointmentsStore(JsonStore):
    """Class for the management of the json file for the appointments"""
    class __AppointmentsStore(JsonStore):
        """Private Class for applying the Singleton Pattern"""
        _FILE_PATH = JSON_FILES_PATH + "store_date.json"
        _ID_FIELD = "_VaccinationAppointment__date_signature"
        INVALID_APPOINTMENT_OBJECT_ERROR = "Invalid appointment object"
        DATE_SIGNATURE_ERROR = "date_signature is not found"

        def add_item(self, item):
            from uc3m_care.data.vaccination_appointment import VaccinationAppointment
            if not isinstance(item, VaccinationAppointment):
                raise VaccineManagementException(self.INVALID_APPOINTMENT_OBJECT_ERROR)
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not AppointmentsStore.instance:
            AppointmentsStore.instance = AppointmentsStore.__AppointmentsStore()

        return AppointmentsStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
