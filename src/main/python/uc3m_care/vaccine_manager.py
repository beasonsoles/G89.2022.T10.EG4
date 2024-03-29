"""Module VaccineManager"""
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""
    class __VaccineManager:
        """Private Class for applying the Singleton Pattern"""
        def __init__(self):
            pass

        @staticmethod
        def request_vaccination_id(patient_id,
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
            # save the patient in store_patient.json
            my_register.register_patient()
            return my_register.patient_sys_id

        @staticmethod
        def get_vaccine_date(input_file):
            """Gets an appointment for a registered patient"""
            my_appointment = VaccinationAppointment.create_appointment_from_json_file(input_file)
            # save the date in store_date.json
            my_appointment.save_appointment()
            return my_appointment.date_signature

        @staticmethod
        def vaccine_patient(date_signature):
            """Register the vaccination of the patient"""
            # check if the appointment is correct
            # if so, save it into store_vaccine.json
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()

        return VaccineManager.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
