from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from .json_store import JsonStore


class PatientJsonStore(JsonStore):
    class __PatientJsonStore(JsonStore):
        _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
        _ID_FIELD = "_VaccinePatientRegister__patient_sys_id"
        PATIENT_REGISTERED_ERROR = "patient_id is registered in store_patient"
        INVALID_PATIENT_OBJECT_ERROR = "Invalid patient object"
        PATIENT_SYS_ID_ERROR = "patient_system_id not found"
        MANIPULATED_DATA_ERROR = "Patient's data have been manipulated"

        def add_item(self, item):
            from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
            if not isinstance(item, VaccinePatientRegister):
                raise VaccineManagementException(self.INVALID_PATIENT_OBJECT_ERROR)
            patient_records = self.find_item_list(item.patient_id, self.PATIENT_ID)
            for patient_record in patient_records:
                if (patient_record[self.REGISTRATION_TYPE] ==
                    item.vaccine_type) and \
                        (patient_record[self.FULL_NAME] ==
                         item.full_name):
                    raise VaccineManagementException(self.PATIENT_REGISTERED_ERROR)
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not PatientJsonStore.instance:
            PatientJsonStore.instance = PatientJsonStore.__PatientJsonStore()

        return PatientJsonStore.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
