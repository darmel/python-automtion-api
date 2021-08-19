import requests
from pprint import pprint
import json
from uuid import uuid4


class PeopleApi:

    def __init__(self, url):
        self.base_url = url

    def get_people(self):
        response = requests.get(url=self.base_url)
        return response

    def get_person(self, person_id):
        path = f'{self.base_url}/{person_id}'
        print(path)
        response = requests.get(url= path)
        pprint(response.json())
        return response

    def create_person(self, payload):
        headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
        response = requests.post(url=self.base_url, data=payload, headers=headers)
        return response
    
    def generate_new_valid_user_data(self):
        unique_lname = str(uuid4())
        person = open("./resources/data/person.json", 'r')
        person_json = json.load(person)
        person_json['lname'] = f'User-{unique_lname}'
        payload = json.dumps(person_json)
        return payload

    def generate_existen_user_data(self):
        person = self.get_people().json()[0]
        lname = person.get('lname')
        fname = person.get('fname')
        body_person = open("./resources/data/person.json", 'r')
        person_json = json.load(body_person)
        person_json['lname'] = lname
        person_json['fname'] = fname
        payload = json.dumps(person_json)
        return payload
