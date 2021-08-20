from pprint import pprint
from assertpy.assertpy import assert_that
#from asertpy.assertpy import assert_that
from apis.people_api import PeopleApi
from config import BASE_URL
from uuid import uuid4
import json
import random


class TestPeopleApi:
    def setup_class(self):
        self.api_people = PeopleApi(url=BASE_URL)


    def test_user_by_id(self):
        '''Verificar que la persona con id = 1 tiene el nombre Doug '''
        response = self.api_people.get_person(1)
        pprint(response.json())
        assert_that(response.status_code).is_equal_to(200)
        person = response.json()
        print(person)
        assert_that(person.get('fname')).is_equal_to('Doug')


    def test_verify_user_list_contain_Doug(self):
        '''Verificar que en el listado de personas existe un elemento cuyo fname = Doug'''
        response = self.api_people.get_people()
        fname = [persona['fname'] for persona in response.json()]
        print(fname)
        assert_that(fname).contains('Doug')

    def test_verify_new_user_can_be_added(self):
        unique_lname = str(uuid4())
        payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"TAU1",
        "lname": f"User1 {unique_lname}"
        })
        #payload = self.api_people.generate_new_valid_user_data() #reemplazamos las lineas comentadas por esta linea que llama al methodo generate new valid user data
        response = self.api_people.create_person(payload)
        assert_that(response.status_code).is_equal_to(204) #status code de POST Create es 204 no 200

    def test_verify_new_user_can_not_be_added(self):
        unique_lname = str(uuid4())
        fname="Kent"
        lname="Brockman"
        payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":f"{fname}",
        "lname":f"{lname}"
        })
        #payload = self.api_people.generate_existen_user_data()
        response = self.api_people.create_person(payload)
        assert_that(response.status_code).is_equal_to(409)
        assert_that(response.json().get('detail')).is_equal_to(f"Person with {fname} {lname} already exists")
        #response = response.json()
        #print(response)
        #assert_that(response.get('detail')).is_equal_to(f"Person with {fname} {lname} already exists")
        
    def test_existen_id_can_be_erased(self):
        personas = self.api_people.get_people()
        #pprint(personas.json())
        delete_id = personas.json()[-1].get('person_id')
        print(personas.json()[-1].get('person_id'))
        #print (delete_id)
        response = self.api_people.delete_person_by_id(delete_id)
        #response = self.api_people.delete_person_by_id(44)
        pprint(response.status_code)
        assert_that(response.status_code).is_equal_to(200)
        assert_that((response.content).decode("utf-8")).is_equal_to(f"Person with id {delete_id} successfully deleted")
        print((response.content).decode("utf-8"))

    def test_verify_no_existen_id_can_not_be_deleted(self):
        delete_id = (str(random.random())).replace('.','').lstrip("0") #replace para sacar el . y lstrip para sacar los 0 a la izquierda
        response = self.api_people.delete_person_by_id(delete_id)
        pprint(response.json())
        assert_that(response.status_code).is_equal_to(404)
        assert_that(response.json().get('detail')).is_equal_to(f"Person not found for id {delete_id}")

    def test_existen_id_can_be_updated(self):
        personas = self.api_people.get_people()
        id = personas.json()[-1].get('person_id')
        print(personas.json()[-1].get('person_id'))
        unique_lname = str(uuid4())
        print(unique_lname)
        payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"TAU1",
        "lname": f"{unique_lname}"
        })
        response = self.api_people.update_person_by_id(id, payload)
        pprint(response.status_code)
        pprint(response.json())
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('fname')).is_equal_to('TAU1')
        assert_that(response.json().get('lname')).is_equal_to(f'{unique_lname}')
        #assert_that((response.content).decode("utf-8")).is_equal_to(f"Person with id {delete_id} successfully deleted")
        #print((response.content).decode("utf-8"))




