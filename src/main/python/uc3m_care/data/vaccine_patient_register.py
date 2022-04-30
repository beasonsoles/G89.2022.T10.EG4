"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
from datetime import datetime
from freezegun import freeze_time
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.attribute.attribute_age import Age
from uc3m_care.data.attribute.attribute_full_name import FullName
from uc3m_care.data.attribute.attribute_patient_id import PatientID
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_registration_type import RegistrationType
from uc3m_care.storage.patients_json_store import PatientJsonStore


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    def __init__(self, patient_id, full_name, registration_type, phone_number, age):
        # we are using the Attribute classes to check their validity
        self.__patient_id = PatientID(patient_id).value
        self.__full_name = FullName(full_name).value
        self.__registration_type = RegistrationType(registration_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__age = Age(age).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        # self.__time_stamp = 1645542405.232003
        self.__patient_sys_id = hashlib.md5(self.__str__().encode()).hexdigest()

    @classmethod
    def create_patient_from_patient_system_id(cls, patient_system_id):
        """Generates a patient class if it coincides with the given patient system id"""
        # check if the patient exists in the storage json file
        patient_store = PatientJsonStore()
        patient_found = patient_store.find_item(patient_system_id)
        if patient_found is None:
            raise VaccineManagementException(patient_store.PATIENT_SYS_ID_ERROR)
        # if the patient exists, create a 'cls' instance with its data
        guid = patient_found[PatientJsonStore.PATIENT_ID]
        name = patient_found[PatientJsonStore.FULL_NAME]
        reg_type = patient_found[PatientJsonStore.REGISTRATION_TYPE]
        phone = patient_found[PatientJsonStore.REGISTER_PHONE_NUMBER]
        age = patient_found[PatientJsonStore.AGE]
        patient_timestamp = patient_found[PatientJsonStore.TIME_STAMP]
        # set the date when the patient was registered for checking the md5
        freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
        freezer.start()
        patient = cls(guid, name, reg_type, phone, age)
        freezer.stop()
        if patient.patient_system_id != patient_system_id:
            raise VaccineManagementException(patient_store.MANIPULATED_DATA_ERROR)
        return patient

    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    def register_patient(self):
        """Method for saving the patients store"""
        patient_store = PatientJsonStore()
        patient_store.add_item(self)
        return True

    @property
    def full_name(self):
        """Property representing the name and the surname of
        the person who request the registration"""
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @property
    def vaccine_type(self):
        """Property representing the type vaccine"""
        return self.__registration_type

    @vaccine_type.setter
    def vaccine_type(self, value):
        self.__registration_type = value

    @property
    def phone_number(self):
        """Property representing the requester's phone number"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def patient_id(self):
        """Property representing the requester's UUID"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def time_stamp(self):
        """Read-only property that returns the timestamp of the request"""
        return self.__time_stamp

    @property
    def patient_system_id(self):
        """Returns the md5 signature"""
        return self.__patient_sys_id

    @property
    def patient_age(self):
        """Returns the patient's age"""
        return self.__age

    @property
    def patient_sys_id(self):
        """Property representing the md5 generated"""
        return self.__patient_sys_id
