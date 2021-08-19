

from pprint import pprint
from assertpy.assertpy import assert_that
from api.people_api import PeopleApi
from config import BASE_URL
from uuid import uuid4
import json

class TestPeopleApi:

    def setup_class(self):
        self.api_people = PeopleApi(url=BASE_URL)

    def test_verify_user_list_contain_Kent(self):
        response = self.api_people.get_people()
        fname = [persona['fname'] for persona in response.json()]
        print(fname)
        assert_that(fname).contains('Kent')

    def test_verify_new_user_can_be_added(self):
        '''unique_lname = str(uuid4())
        payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"TAU1",
        "lname": f"User1 {unique_lname}"
        })'''
        payload = self.api_people.generate_new_valid_user_data() #reemplazamos las lineas comentadas por esta linea que llama al methodo generate new valid user data
        response = self.api_people.create_person(payload)
        assert_that(response.status_code).is_equal_to(204)

    def test_verify_new_user_can_not_be_added(self):
        unique_lname = str(uuid4())
        '''payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"Kent",
        "lname": "Brockman"
        })'''
        payload = self.api_people.generate_existen_user_data()
        response = self.api_people.create_person(payload)
        assert_that(response.status_code).is_equal_to(409)

    def test_user_by_id(self):
        response = self.api_people.get_person(1)
        pprint(response.json())
        assert_that(response.status_code).is_equal_to(200)
        person = response.json()
        print(person)
        assert_that(person.get('fname')).is_equal_to('Doug')
        assert_that(person.get('lname')).is_equal_to('Farrell')

