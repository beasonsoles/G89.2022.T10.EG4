"""Module for the VaccinationLog class"""
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore


class VaccinationLog:
    """Class for the VaccinationLog object"""

    def __init__(self):
        pass

    def save_log_entry(self):
        """The method creates a VaccinationJsonStore and inserts the first item"""
        vaccination_log = VaccinationJsonStore()
        vaccination_log.add_item(self)
