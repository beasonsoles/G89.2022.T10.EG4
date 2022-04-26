from datetime import datetime
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore


class VaccinationLog:

    def __init__(self, date_signature):
        self.__date_signature = date_signature
        self.__timestamp = datetime.timestamp(datetime.utcnow())

    def save_log_entry(self):
        vaccination_log = VaccinationJsonStore()
        vaccination_log.add_item(self)
