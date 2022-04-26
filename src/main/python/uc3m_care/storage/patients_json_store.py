from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from .json_store import JsonStore


class PatientJsonStore(JsonStore):
    # class __PatientJsonStore:
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
    _ID_FIELD = "_VaccinePatientRegister__patient_sys_id"
    INVALID_PATIENT_OBJECT_ERROR = "Invalid patient object"

    def add_item(self, item):
        from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
        if not isinstance(item, VaccinePatientRegister):
            raise VaccineManagementException(self.INVALID_PATIENT_OBJECT_ERROR)
        patient_found = False
        patient_records = PatientJsonStore.find_item_list(item.patient_id,
                                                          "_VaccinePatientRegister__patient_id")
        for patient_record in patient_records:
            if (patient_record["_VaccinePatientRegister__registration_type"] ==
                item.vaccine_type) and \
                    (patient_record["_VaccinePatientRegister__full_name"] ==
                     item.full_name):
                raise VaccineManagementException("patient_id is registered in store_patient")
        if not patient_found:
            super().add_item(item)

    # instance = None
    #
    # def __new__(cls):
    #     if not PatientJsonStore.instance:
    #         PatientJsonStore.instance = PatientJsonStore.__PatientJsonStore()
    #
    #     return PatientJsonStore.instance
    #
    # def __getattr__(self, name):
    #     return getattr(self.instance, name)
    #
    # def __setattr__(self, name, value):
    #     return setattr(self.instance, name, value)
