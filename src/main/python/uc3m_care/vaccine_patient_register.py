"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
import re
import uuid
from datetime import datetime
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.vaccine_manager_config import JSON_FILES_PATH
from .data.attribute.attribute_age import Age
from .data.attribute.attribute_full_name import FullName
from .data.attribute.attribute_patient_id import PatientID
from .data.attribute.attribute_phone_number import PhoneNumber
from .data.attribute.attribute_registration_type import RegistrationType


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    # pylint: disable = too-many-arguments
    def __init__(self, patient_id, full_name, registration_type, phone_number, age):
        self.__patient_id = PatientID(patient_id).value
        self.__full_name = FullName(full_name).value
        self.__registration_type = RegistrationType(registration_type).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__age = Age(age).value
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        # self.__time_stamp = 1645542405.232003
        self.__patient_sys_id = hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @staticmethod
    def register_patient(data):
        """Method for saving the patients store"""
        patient_store = JSON_FILES_PATH + "store_patient.json"
        # first read the file
        try:
            with open(patient_store, "r", encoding="utf-8", newline="") as file:
                patients = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            patients = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        found = False
        for patient in patients:
            if patient["_VaccinePatientRegister__patient_id"] == data.patient_id and \
                    patient["_VaccinePatientRegister__registration_type"] == data.vaccine_type and \
                    patient["_VaccinePatientRegister__full_name"] == data.full_name:
                found = True
        if found is False:
            patients.append(data.__dict__)
            try:
                with open(patient_store, "w", encoding="utf-8", newline="") as file:
                    json.dump(patients, file, indent=2)
            except FileNotFoundError as exception:
                raise VaccineManagementException("Wrong file or file path") from exception
        else:
            raise VaccineManagementException("patient_id is registered in store_patient")
        return True

    @staticmethod
    def register_patient_fast(data):
        """Method for saving the patients store"""
        patients_store = JSON_FILES_PATH + "store_patient.json"
        with open(patients_store, "r+", encoding="utf-8", newline="") as file:
            patients = json.load(file)
            patients.append(data.__dict__)
            file.seek(0)
            json.dump(patients, file, indent=2)

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
