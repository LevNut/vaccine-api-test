"""Teeranut Sawanyawat 6210545491"""

import unittest
import requests

from decouple import config

url = config('URL')


def create_registration(citizen_id, name, surname, birth_date, occupation, phone_number, is_risk, address):
    """Create Registration of the User to the website database."""
    return f"citizen_id={citizen_id}" \
           f"&name={name}" \
           f"&surname={surname}" \
           f"&birth_date={birth_date}" \
           f"&occupation={occupation}" \
           f"&phone_number={phone_number}" \
           f"&is_risk={is_risk}" \
           f"&address={address}"


class ProjectApiTestCase(unittest.TestCase):
    """Test case for Project API from https://wcg-apis.herokuapp.com/"""

    def setUp(self) -> None:
        path = create_registration("1234567899999", "Edward", "Newgate",
                                   "02/02/2000", "Business CEO",
                                   "0877777777", "False", "New World")

        requests.post(url=url + f"/registration?{path}")

    def test_fetch_user_personal_info(self):
        """Testing if we are able to fetch the data from the WCG database."""
        response = requests.get(url + f"/registration/{1234567899999}")
        self.assertEqual("1234567899999", response.json()["citizen_id"])

    def test_registration_without_right_amount_of_citizen_id(self):
        """Testing if we are able to put a string in the citizen id."""
        path = create_registration("110548736574", "Josh", "Newgate",
                                   "12/11/1999", "Guard",
                                   "0912341945", "False", "Middle World",)
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_registration_with_special_character_in_citizen_id(self):
        """Testing if we are able to put a string in the citizen id."""
        path = create_registration("Ω≈ç√∂®øπ˚≈π˚ß", "Buggy", "Oldgate",
                                   "12/04/1890", "Clown",
                                   "0813444433", "False", "Old World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_registration_with_string_in_citizen_id(self):
        """Testing if we are able to put a string in the citizen id."""
        path = create_registration("ThisIsText", "Marry", "Newgate",
                                   "01/01/2000", "Maid",
                                   "0721231234", "False", "New World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid citizen ID", response.json()["feedback"])

    def test_registration_with_string_in_birth_date(self):
        """Testing if we are able to put a string in the citizen id."""
        path = create_registration("1103045746883", "Margo", "Newgate",
                                   "05Feb2010", "Waiter",
                                   "0812342344", "False", "Old World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid birth date format", response.json()["feedback"])

    def test_registration_with_too_old_datetime(self):
        """Testing if the birth date can be extremely old."""
        path = create_registration("5555555555555", "Seft", "Newgate",
                                   "09/11/1000", "Taxi Driver",
                                   "0972031234", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid birth date format", response.json()["feedback"])

    def test_registration_with_non_existed_datetime(self):
        """Testing if the birth date can be extremely old."""
        path = create_registration("6666666666666", "Lore", "Oldgate",
                                   "32/02/2000", "Doctor",
                                   "0934567891", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: invalid birth date format", response.json()["feedback"])

    def test_registration_with_special_character_in_name_and_surname(self):
        """Testing if we are able to put a string in the citizen id."""
        path = create_registration("1104358630932", "Ace©", "Newgateπ",
                                   "08/02/2005", "Cook",
                                   "0852345678", "False", "Weird World")
        response = requests.post(url + f"/registration?{path}")
        self.assertNotEqual(200, response.status_code)

    def test_registration_with_integer_in_name_and_surname(self):
        """Testing if we are able to put an integer in the name and surname."""
        path = create_registration("2222222222222", "123", "456",
                                   "03/03/1990", "Math Professor",
                                   "0987654321", "False", "Old World")
        response = requests.post(url + f"/registration?{path}")
        self.assertNotEqual(200, response.status_code)

    def test_registration_with_integer_in_occupation(self):
        """Testing if we are able to put an integer in the occupation."""
        path = create_registration("3333333333333", "Teach", "Oldgate",
                                   "06/06/1890", "12345",
                                   "0934567890", "False", "Old World")
        response = requests.post(url + f"/registration?{path}")
        self.assertNotEqual(200, response.status_code)

    def test_empty_citizen_id_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("", "John", "Cena",
                                   "25/12/2000", "Scrum Master",
                                   "0678654390", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_name_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1234567891011", "", "Cena",
                                   "25/12/2000", "Scrum Master",
                                   "0935672346", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_surname_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1234567891011", "John", "",
                                   "25/12/2000", "Scrum Master",
                                   "0805467778", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_birth_date_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1234567891011", "John", "Cena",
                                   "", "Scrum Master",
                                   "0911111111", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_occupation_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1234567891011", "John", "Cena",
                                   "25/12/2000", "",
                                   "0922222222", "False", "Middle World")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_address_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1234567891011", "John", "Cena",
                                   "25/12/2000", "Scrum Master",
                                   "0933333333", "False", "")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_empty_phone_number_of_the_user(self):
        """Testing if we are able to insert empty data during registration."""
        path = create_registration("1999992222888", "Cena", "John",
                                   "28/12/1990", "Product Owner",
                                   "", "True", "WWE stadium")
        response = requests.post(url + f"/registration?{path}")
        self.assertEqual("registration failed: missing some attribute", response.json()["feedback"])

    def test_delete_data_of_user_info(self):
        """Testing if we are able to delete personal info of other user."""
        response = requests.delete(url + f"/citizen?citizen_id={2222222222222}")
        self.assertNotEqual(200, response.status_code)


