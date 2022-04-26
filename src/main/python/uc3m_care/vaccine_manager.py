"""Module """
from uc3m_care.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.vaccination_appoinment import VaccinationAppoinment


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
        my_appointment = VaccinationAppoinment.create_appointment_from_json_file(input_file)
        # save the date in store_date.json
        my_appointment.save_appointment()
        return my_appointment.date_signature

    def vaccine_patient(self, date_signature):
        """Register the vaccination of the patient"""
        appointment = VaccinationAppoinment.get_appointment_from_date_signature(date_signature)
        return appointment.register_vaccination()
