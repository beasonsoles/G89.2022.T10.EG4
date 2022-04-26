from uc3m_care.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.vaccine_management_exception import VaccineManagementException
from .json_store import JsonStore


class PatientJsonStore(JsonStore):
    _FILE_PATH = JSON_FILES_PATH + "store_patient.json"
    _ID_FIELD = "_VaccinePatientRegister__patient_sys_id"

    def add_item(self, item):
        from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
        if not isinstance(item, VaccinePatientRegister):
            raise VaccineManagementException("Invalid patient object")
        patient_found = False
        patient_records = self.find_item_list(item.patient_id,
                                              "_VaccinePatientRegister__patient_id")
        for patient_record in patient_records:
            if (patient_record["_VaccinePatientRegister__registration_type"] ==
                item.vaccine_type) and \
                    (patient_record["_VaccinePatientRegister__full_name"] ==
                     item.full_name):
                patient_found = True
        if not patient_found:
            super().add_item(item)
