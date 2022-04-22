"""MODULE: access_request. Contains the access request class"""
import hashlib
import json
import re
import uuid
from datetime import datetime
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.vaccine_manager_config import JSON_FILES_PATH


class VaccinePatientRegister:
    """Class representing the register of the patient in the system"""
    # pylint: disable = too-many-arguments
    def __init__(self, patient_id, full_name, registration_type, phone_number, age):
        self.__patient_id = self.validate_guid(patient_id)
        self.__full_name = self.validate_full_name(full_name)
        self.__registration_type = self.validate_registration_type(registration_type)
        self.__phone_number = self.validate_phone_number(phone_number)
        self.__age = self.validate_age(age)
        justnow = datetime.utcnow()
        self.__time_stamp = datetime.timestamp(justnow)
        # self.__time_stamp = 1645542405.232003
        self.__patient_sys_id = hashlib.md5(self.__str__().encode()).hexdigest()

    def __str__(self):
        return "VaccinePatientRegister:" + json.dumps(self.__dict__)

    @staticmethod
    def validate_guid(guid):
        """Method for validating uuid v4"""
        try:
            my_uuid = uuid.UUID(guid)
            myregex = re.compile(r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]" +
                                 "{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$",
                                 re.IGNORECASE)
            result = myregex.fullmatch(my_uuid.__str__())
            if not result:
                raise VaccineManagementException("UUID invalid")
        except ValueError as val_er:
            raise VaccineManagementException("Id received is not a UUID") from val_er
        return guid

    @staticmethod
    def validate_registration_type(registration_type):
        """Checks the validity of the registration type"""
        myregex = re.compile(r"(Regular|Family)")
        result = myregex.fullmatch(registration_type)
        if not result:
            raise VaccineManagementException("Registration type is nor valid")
        return registration_type

    @staticmethod
    def validate_full_name(full_name):
        """Checks the validity of the full name"""
        myregex = re.compile(r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$")
        result = myregex.fullmatch(full_name)
        if not result:
            raise VaccineManagementException("name surname is not valid")
        return full_name

    @staticmethod
    def validate_phone_number(phone_number):
        """Checks the validity of the phone number"""
        myregex = re.compile(r"^(\+)[0-9]{11}")
        result = myregex.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException("phone number is not valid")
        return phone_number

    @staticmethod
    def validate_age(age):
        """Checks the validity of the age"""
        if age.isnumeric():
            if int(age) < 6 or int(age) > 125:
                raise VaccineManagementException("age is not valid")
        else:
            raise VaccineManagementException("age is not valid")
        return age

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
