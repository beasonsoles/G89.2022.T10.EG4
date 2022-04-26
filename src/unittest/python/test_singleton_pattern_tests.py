import unittest
from uc3m_care import VaccineManager
from uc3m_care.storage.appointments_store import AppointmentsStore
from uc3m_care.storage.patients_json_store import PatientJsonStore
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore


class SingletonTestCases(unittest.TestCase):
    def test_vaccine_manager_singleton(self):
        vm1 = VaccineManager()
        vm2 = VaccineManager()
        vm3 = VaccineManager()
        vm4 = VaccineManager()
        self.assertEqual(vm1, vm2)
        self.assertEqual(vm1, vm3)
        self.assertEqual(vm1, vm4)

    def test_appointments_store_singleton(self):
        as1 = AppointmentsStore()
        as2 = AppointmentsStore()
        as3 = AppointmentsStore()
        as4 = AppointmentsStore()
        self.assertEqual(as1, as2)
        self.assertEqual(as1, as3)
        self.assertEqual(as1, as4)

    def test_patients_json_store_singleton(self):
        ps1 = PatientJsonStore()
        ps2 = PatientJsonStore()
        ps3 = PatientJsonStore()
        ps4 = PatientJsonStore()
        self.assertEqual(ps1, ps2)
        self.assertEqual(ps1, ps3)
        self.assertEqual(ps1, ps4)

    def test_vaccination_json_store_singleton(self):
        vs1 = VaccinationJsonStore()
        vs2 = VaccinationJsonStore()
        vs3 = VaccinationJsonStore()
        vs4 = VaccinationJsonStore()
        self.assertEqual(vs1, vs2)
        self.assertEqual(vs1, vs3)
        self.assertEqual(vs1, vs4)


if __name__ == "__main__":
    unittest.main()
