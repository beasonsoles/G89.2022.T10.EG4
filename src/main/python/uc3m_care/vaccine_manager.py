"""Module """
import datetime
import re
import json
from datetime import datetime
from typing import List

from freezegun import freeze_time

from . import VaccinePatientRegister
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
from .vaccine_manager_config import JSON_FILES_PATH


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    def __init__(self):
        pass

    # pylint: disable=too-many-arguments
    def request_vaccination_id(self,
                               patient_id,
                               name_surname,
                               registration_type,
                               phone_number,
                               age):
        """Register the patient into the patients file"""
        my_register = VaccinePatientRegister(patient_id,
                                             name_surname,
                                             registration_type,
                                             phone_number,
                                             age)
        myregex = re.compile(r"(Regular|Family)")
        result = myregex.fullmatch(registration_type)
        if not result:
            raise VaccineManagementException("Registration type is nor valid")

        myregex = re.compile(r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$")
        result = myregex.fullmatch(name_surname)
        if not result:
            raise VaccineManagementException ("name surname is not valid")

        myregex = re.compile(r"^(\+)[0-9]{11}")
        result = myregex.fullmatch(phone_number)
        if not result:
            raise VaccineManagementException("phone number is not valid")
        if age.isnumeric():
            if int(age) < 6 or int(age) > 125:
                raise VaccineManagementException("age is not valid")
        else:
            raise VaccineManagementException("age is not valid")
        if my_register.validate_guid(patient_id):
            my_patient = VaccinePatientRegister(patient_id,
                                                name_surname,
                                                registration_type,
                                                phone_number,
                                                age)
        my_register.register_patient(my_patient)

        return my_patient.patient_sys_id

    def get_vaccine_date(self, input_file):
        """Gets an appointment for a registered patient"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            # file is not found
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        my_register = VaccinePatientRegister(data["_VaccinePatientRegister__patient_id"],
                                             data["_VaccinePatientRegister__full_name"],
                                             data["_VaccinePatientRegister__registration_type"],
                                             data["_VaccinePatientRegister__phone_number"],
                                             data["_VaccinePatientRegister__age"])
        # check all the information
        try:
            myregex = re.compile(r"[0-9a-fA-F]{32}$")
            result = myregex.fullmatch(data["PatientSystemID"])
            if not result:
                raise VaccineManagementException("patient system id is not valid")
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception

        try:
            myregex = re.compile(r"^(\+)[0-9]{11}")
            result = myregex.fullmatch(data["ContactPhoneNumber"])
            if not result:
                raise VaccineManagementException("phone number is not valid")
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception
        patient_store = JSON_FILES_PATH + "store_patient.json"

        with open(patient_store, "r", encoding="utf-8", newline="") as file:
            patients = json.load(file)
        found = False
        for patient in patients:
            if patient["_VaccinePatientRegister__patient_sys_id"] == data["PatientSystemID"]:
                found = True
                # retrieve the patients data
                guid = patient["_VaccinePatientRegister__patient_id"]
                name = patient["_VaccinePatientRegister__full_name"]
                reg_type = patient["_VaccinePatientRegister__registration_type"]
                phone = patient["_VaccinePatientRegister__phone_number"]
                patient_timestamp = patient["_VaccinePatientRegister__time_stamp"]
                age = patient["_VaccinePatientRegister__age"]
                # set the date when the patient was registered for checking the md5
                freezer = freeze_time(datetime.fromtimestamp(patient_timestamp).date())
                freezer.start()
                patient = VaccinePatientRegister(guid, name, reg_type, phone, age)
                freezer.stop()
                if patient.patient_system_id != data["PatientSystemID"]:
                    raise VaccineManagementException("Patient's data have been manipulated")
        if not found:
            raise VaccineManagementException("patient_system_id not found")

        signature = VaccinationAppoinment(guid, data["PatientSystemID"],
                                          data["ContactPhoneNumber"], 10)

        # save the date in store_date.json

        my_register.save_appointment(signature)

        return signature.date_signature

    def vaccine_patient(self, date_signature):
        """Register the vaccination of the patient"""
        # check if this date is in store_date
        appointment_store = JSON_FILES_PATH + "store_date.json"
        # first read the file
        try:
            with open(appointment_store, "r", encoding="utf-8", newline="") as file:
                appointments = json.load(file)
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        except FileNotFoundError as exception:
            raise VaccineManagementException("Store_date not found") from exception
        my_appointment = VaccinationAppoinment(
                                    appointments["_VaccinationAppoinment__patient_id"],
                                    appointments["_VaccinationAppoinment__patient_sys_id"],
                                    appointments["_VaccinationAppoinment__phone_number"],
                                    appointments["_VaccinationAppoinment__appoinment_date"])
        my_appointment.validate_date_signature(date_signature)
        # search this date_signature
        found = False
        for appointment in appointments:
            if appointment["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                date_time = appointment["_VaccinationAppoinment__appoinment_date"]
        if not found:
            raise VaccineManagementException("date_signature is not found")

        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(date_time).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

        vaccination_store = JSON_FILES_PATH + "store_vaccine.json"

        try:
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                appointments = json.load(file)
        except FileNotFoundError as exception:
            # file is not found , so  init my data_list
            appointments = []
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception

            # append the date
        appointments.append(date_signature.__str__())
        appointments.append(datetime.utcnow().__str__())
        try:
            with open(vaccination_store, "w", encoding="utf-8", newline="") as file:
                json.dump(appointments, file, indent=2)
        except FileNotFoundError as exception:
            raise VaccineManagementException("Wrong file or file path") from exception
        return True
