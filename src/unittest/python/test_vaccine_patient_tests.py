"""Module for testing vaccine_patient"""
from unittest import TestCase
import os
import hashlib
import json
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH
from uc3m_care import JSON_FILES_RF2_PATH
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore


class TestVaccinePatient(TestCase):
    """Class for testing vaccine patient"""
    @freeze_time("2022-03-08")
    def setUp(self):
        """first prepare the stores"""
        patient_store = JSON_FILES_PATH + "store_patient.json"
        appointment_store = JSON_FILES_PATH + "store_date.son"

        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        if os.path.isfile(patient_store):
            os.remove(patient_store)
        if os.path.isfile(appointment_store):
            os.remove(appointment_store)

        # add patient and date in the store
        my_manager = VaccineManager()
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima", "Regular",
                                          "+34123456789", "6")
        my_manager.get_vaccine_date(file_test)

        my_manager.request_vaccination_id("57c811e5-3f5a-4a89-bbb8-11c0464d53e6",
                                          "minombre tieneuncharmenosqmax", "Family",
                                          "+34333456789", "7")
        file_test = JSON_FILES_RF2_PATH + "test_ok_2.json"

        my_manager.get_vaccine_date(file_test)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_ok(self):
        """basic path , signature is found , and date = today"""
        my_manager = VaccineManager()
        signature = my_manager.vaccine_patient(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertTrue(signature)
        vaccination_log = VaccinationJsonStore()
        vaccination_entry = vaccination_log.find_item("5a06c7bede3d584e934e2f5bd3861e625cb"
                                                      "31937f9f1a5362a51fbbf38486f1c")
        self.assertIsNotNone(vaccination_entry)

    @freeze_time("2022-04-18")
    def test_vaccine_patient_no_date(self):
        """path signature is found , and date is not today"""
        vaccination_store = JSON_FILES_PATH + "store_vaccine.json"
        my_manager = VaccineManager()

        # read the file  to compare
        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "Today is not the date")

        # read the file again to compare
        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_bad_date_signature(self):
        """path signature is not valid format , only 63 characters"""
        vaccination_store = JSON_FILES_PATH + "store_vaccine.json"
        my_manager = VaccineManager()
        # read the file  to compare

        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "date_signature format is not valid")

        # read the file again to compare
        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_not_found_date_signature(self):
        """path: signature is not found in store_date"""
        vaccination_store = JSON_FILES_PATH + "store_vaccine.json"
        my_manager = VaccineManager()
        # read the file  to compare

        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_original = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_original = ""

        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "7a8403d8605804cf2534fd7885940f3c3d8ec60ba578bc158b5dc2b9fb68d524")
        self.assertEqual(context_manager.exception.message, "date_signature is not found")

        # read the file again to compare
        if os.path.isfile(vaccination_store):
            with open(vaccination_store, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(file.__str__().encode()).hexdigest()
        else:
            hash_new = ""

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-18")
    def test_vaccine_patient_no_store_date(self):
        """path: store_date is not found, so remove store_date.json"""
        appointment_store = JSON_FILES_PATH + "store_date.json"
        if os.path.isfile(appointment_store):
            os.remove(appointment_store)

        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "Store_date not found")

    @freeze_time("2022-03-18")
    def test_vaccine_patient_store_date_is_empty(self):
        """for testing: store_date is empty"""
        # write a store_date empty
        appointment_store = JSON_FILES_PATH + "store_date.json"
        vaccinations = []
        with open(appointment_store, "w", encoding="utf-8", newline="") as file:
            json.dump(vaccinations, file, indent=2)

        my_manager = VaccineManager()
        with self.assertRaises(VaccineManagementException) as context_manager:
            my_manager.vaccine_patient(
                "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(context_manager.exception.message, "date_signature is not found")
