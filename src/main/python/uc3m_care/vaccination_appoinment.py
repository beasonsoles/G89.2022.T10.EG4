"""Contains the class Vaccination Appointment"""
import hashlib
import json
import re
from datetime import datetime
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.vaccine_manager_config import JSON_FILES_PATH


# pylint: disable=too-many-instance-attributes
class VaccinationAppoinment:
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, guid, patient_sys_id, patient_phone_number, days):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_id = guid
        self.__patient_sys_id = self.validate_system_id(patient_sys_id)
        self.__phone_number = self.validate_phone_number(patient_phone_number)
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if days == 0:
            self.__appoinment_date = 0
        else:
            # timestamp is represented in seconds.microseconds
            # age must be expressed in seconds to be added to the timestamp
            self.__appoinment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appoinment_date.__str__() + "}"

    @staticmethod
    def validate_date_signature(signature):
        """Method for validating sha256 values"""
        myregex = re.compile(r"[0-9a-fA-F]{64}$")
        result = myregex.fullmatch(signature)
        if not result:
            raise VaccineManagementException("date_signature format is not valid")

    @staticmethod
    def validate_system_id(system_id):
        myregex = re.compile(r"[0-9a-fA-F]{32}$")
        result = myregex.fullmatch(system_id)
        if not result:
            raise VaccineManagementException("patient system id is not valid")
        return system_id

    @staticmethod
    def validate_phone_number(phone_number):
        myregex = re.compile(r"^(\+)[0-9]{11}")
        result = myregex.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException("phone number is not valid")
        return phone_number

    @staticmethod
    def save_appointment(signature):
        """Saves the appointment into a file"""
        appointment_store = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(appointment_store, "r", encoding="utf-8", newline="") as file:
                appointments = json.load(file)
        except FileNotFoundError:
            # file is not found , so  init my data_list
            appointments = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

        # append the date
        appointments.append(signature.__dict__)

        try:
            with open(appointment_store, "w", encoding="utf-8", newline="") as file:
                json.dump(appointments, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception

    @property
    def patient_id(self):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number(self):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @property
    def vaccination_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def appoinment_date(self):
        """Returns the vaccination date"""
        return self.__appoinment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature
