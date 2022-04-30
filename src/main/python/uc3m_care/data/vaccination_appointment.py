"""Contains the class Vaccination Appointment"""
import hashlib
from datetime import datetime
from freezegun import freeze_time
from uc3m_care.data.attribute.AttributeDateSignature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.attribute.AttributePatientSystemId import PatientSystemID
from uc3m_care.data.attribute.AttributePhoneNumber import PhoneNumber
from uc3m_care.storage.appointments_store import AppointmentsStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser


# pylint: disable=too-many-instance-attributes


class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, patient_sys_id, patient_phone_number, days):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemID(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if days == 0:
            self.__appointment_date = 0
        else:
            # timestamp is represented in seconds.microseconds
            # age must be expressed in seconds to be added to the timestamp
            self.__appointment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature
        self.NOT_TODAY_ERROR = "Today is not the date"


    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    def save_appointment(self):
        """Saves the appointment into a file"""
        appointments_store = AppointmentsStore()
        appointments_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature):
        appointments_store = AppointmentsStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException(appointments_store.DATE_SIGNATURE_ERROR)
        freezer = freeze_time(datetime.fromtimestamp(
            appointment_record[AppointmentsStore.ISSUED_DATE]))
        freezer.start()
        appointment = cls(appointment_record[AppointmentsStore.PATIENT_SYSTEM_ID],
                          appointment_record[AppointmentsStore.APPOINTMENT_PHONE_NUMBER], 10)
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file):
        appointment_parser = AppointmentJsonParser(json_file)
        my_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            10)
        return my_appointment

    def is_valid_today(self):
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException(self.NOT_TODAY_ERROR)
        return True

    def register_vaccination(self):
        if self.is_valid_today():
            vaccination_entry = VaccinationLog(self.date_signature)
            vaccination_entry.save_log_entry()
        return True

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
        self.__phone_number = PhoneNumber(value).value

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
    def appointment_date(self):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature
