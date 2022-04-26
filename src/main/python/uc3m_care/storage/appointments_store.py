from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.json_store import JsonStore


class AppointmentsStore(JsonStore):
    # class __AppointmentsStore:
    _FILE_PATH = JSON_FILES_PATH + "store_date.json"
    _ID_FIELD = "_VaccinationAppointment__date_signature"
    ERROR_INVALID_APPOINTMENT_OBJECT = "Invalid appointment object"

    def add_item(self, item):
        from uc3m_care.data.vaccination_appointment import VaccinationAppointment
        if not isinstance(item, VaccinationAppointment):
            raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
        super().add_item(item)

    # instance = None
    #
    # def __new__(cls):
    #     if not AppointmentsStore.instance:
    #         AppointmentsStore.instance = AppointmentsStore.__AppointmentsStore()
    #
    #     return AppointmentsStore.instance
    #
    # def __getattr__(self, name):
    #     return getattr(self.instance, name)
    #
    # def __setattr__(self, name, value):
    #     return setattr(self.instance, name, value)

