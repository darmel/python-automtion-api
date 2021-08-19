import requests
from pprint import pprint
from assertpy.assertpy import assert_that
import json
from config import BASE_URL
from uuid import uuid4
import os

'''def test_disabling_capturing(capsys):
    print('this output is captured')
    with capsys.disabled():
        print('output not captured, going directly to sys.stdout')
    print('this output is also captured')'''
    
def test_get_people():
    url = "http://127.0.0.1:5000/api/people"
    response = requests.get(url = url)
    personas = response.json()
    '''print("\nel codigo de estado es: ", end= '')
    print(response.status_code)'''
    pprint(response.json() )
    assert_that(response.status_code).is_equal_to(200)
    fname = [persona['fname'] for persona in personas]
    print(fname)
    assert_that(fname).contains('Kent')

#def test_post_people():
def test_person_already_exist_can_not_be_added():
    #url = "http://127.0.0.1:5000/api/people" #lo reemplazo por BASE_URL del archifo config-py
    payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"TAU1",
        "lname":"User1"
    })
    headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
    response = requests.post(url=BASE_URL, data=payload, headers=headers)
    pprint(response.json())
    assert_that(response.status_code).is_equal_to(409)
    assert_that(response.json()['detail']).is_equal_to('Person with TAU1 User1 already exists')


def test_new_person_can_be_added():
    unique_lname = str(uuid4())
    payload = json.dumps({  #json.dumps transforma el diccionario en un objeto tipo json
        "fname":"TAU1",
        "lname": f"User1 {unique_lname}"
    })
    headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
    response = requests.post(url=BASE_URL, data=payload, headers=headers)
    #pprint(response.json()) la respuesta esta vacia, por eso falla si quiero mostrar 
    assert_that(response.status_code).is_equal_to(204)
    people = requests.get(url=BASE_URL).json()
    #pprint(people)
    lname = [persona['lname'] for persona in people]
    assert_that(lname).contains(f'User1 {unique_lname}')


def test_new_person_can_be_added_from_file():
    unique_lname = str(uuid4())
    person = open("./resources/data/person.json", 'r')
    person_json = json.load(person)
    person_json['lname'] = f'User-{unique_lname}'
    payload = json.dumps(person_json)
    headers = {'Content-Type':'application/json',
                'Accept':'application/json'}
    response = requests.post(url=BASE_URL, data=payload, headers=headers)
    #pprint(response.json()) la respuesta esta vacia, por eso falla si quiero mostrar 
    assert_that(response.status_code).is_equal_to(204)
    people = requests.get(url=BASE_URL).json()
    #pprint(people)
    lname = [persona['lname'] for persona in people]
    assert_that(lname).contains(f'User-{unique_lname}')
