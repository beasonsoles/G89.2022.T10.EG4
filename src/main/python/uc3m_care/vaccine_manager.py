"""Module """
import datetime
import json
from datetime import datetime
from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.vaccine_management_exception import VaccineManagementException
from uc3m_care.vaccination_appoinment import VaccinationAppoinment
from uc3m_care.vaccine_manager_config import JSON_FILES_PATH


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
        my_register.register_patient()
        return my_register.patient_sys_id

    def get_vaccine_date(self, input_file):
        """Gets an appointment for a registered patient"""
        # open the files
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as exception:
            raise VaccineManagementException("File is not found") from exception
        except json.JSONDecodeError as exception:
            raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from exception
        # check the information
        try:
            patient_sys_id = data["PatientSystemID"]
        except KeyError as exception:
            raise VaccineManagementException("Bad label patient_id") from exception
        try:
            patient_phone_number = data["ContactPhoneNumber"]
        except KeyError as exception:
            raise VaccineManagementException("Bad label contact phone") from exception
        my_appointment = VaccinationAppoinment(patient_sys_id, patient_phone_number, 10)
        # save the date in store_date.json
        my_appointment.save_appointment()
        return my_appointment.date_signature

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
        found = False
        for appointment in appointments:
            if appointment["_VaccinationAppoinment__date_signature"] == date_signature:
                found = True
                date_time = appointment["_VaccinationAppoinment__appoinment_date"]
                my_appointment = VaccinationAppoinment(
                    appointment["_VaccinationAppoinment__patient_sys_id"],
                    appointment["_VaccinationAppoinment__phone_number"],
                    appointment["_VaccinationAppoinment__appoinment_date"])
                my_appointment.validate_date_signature(date_signature)
        if not found:
            raise VaccineManagementException("date_signature is not found")

        # search this date_signature
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
