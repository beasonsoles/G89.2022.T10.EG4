"""UC3M Care MODULE WITH ALL THE FEATURES REQUIRED FOR ACCESS CONTROL"""

from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RF2_PATH
from uc3m_care.data.vaccination_appointment import VaccinationAppointment
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.vaccine_manager import VaccineManager
