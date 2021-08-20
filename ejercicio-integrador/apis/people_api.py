import requests
from pprint import pprint
import json
from uuid import uuid4


class PeopleApi:

    def __init__(self, url):
        self.base_url = url

    '''leer una persona'''
    def get_person(self, person_id):
        path = f'{self.base_url}/{person_id}'
        print(path)
        response = requests.get(url= path)
        pprint(response.json())
        return response

    '''leer todas las personas'''
    def get_people(self):
        response = requests.get(url=self.base_url)
        return response

    '''crear una persona'''
    def create_person(self, payload):
        headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
        response = requests.post(url=self.base_url, data=payload, headers=headers)
        return response

    def delete_person_by_id(self, id):
        self.id = str(id)
        headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
        response = requests.delete(url=self.base_url+'/'+self.id, headers=headers)
        return response

    def update_person_by_id(self, id, payload):
        self.id = str(id)
        headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
        response = requests.put(url=self.base_url+'/'+self.id, data=payload, headers=headers)
        return response


