# 1: Import libraries need for the test
from application.models import Entry, User
import datetime as datetime
import pytest
from flask import json

# TESTING FOR ENTRY CLASS
# Unit Test
# 2: Parametrize section contains the data for the test


@pytest.mark.parametrize("entrylist", [['apple.png', 'rotten banana'],
                                       # Test float arguments
                                       ['banana.png', 'fresh banana']
                                       ])
# 3: Write the test function pass in the arguments
def test_EntryClass(entrylist, capsys):
    with capsys.disabled():
        print(entrylist)
        now = datetime.datetime.utcnow()
        new_entry = Entry(filename=entrylist[0],
                          prediction=entrylist[1],
                          predicted_on=now)

        assert new_entry.filename.endswith(
            '.png') and type(new_entry.filename) == str
        assert (new_entry.prediction.startswith('fresh') or new_entry.prediction.startswith(
            'rotten')) and type(new_entry.prediction) == str
        assert new_entry.predicted_on == now


@pytest.mark.xfail(reason="isinstance(arguments,'str')==False")
@pytest.mark.parametrize("entrylist", [
    [1450, 'fresh banana'],
    ['apple.png', 56]
])
def test_EntryValidation(entrylist, capsys):
    test_EntryClass(entrylist, capsys)

# Test add API


@pytest.mark.parametrize("entrylist", [
    ['lemon.png', 'rotten lemon'],
    ['tomato.png', 'fresh tomato']
])
def test_addAPI(client, entrylist, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        data1 = {'userid': entrylist[2],
                 'filename': entrylist[0],
                 'prediction': entrylist[1]}
        # use client object  to post
        # data is converted to json
        # posting content is specified
        response = client.post('/api/add',
                               data=json.dumps(data1),
                               content_type="application/json",)
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]

# Test get API


@pytest.mark.parametrize("entrylist", [
    [1, 1, 'lemon.png', 'rotten lemon'],
    [2, 1, 'tomato.png', 'fresh tomato']
])
def test_getAPI(client, entrylist, capsys):
    with capsys.disabled():
        response = client.get(f'/api/get/{entrylist[1]}')
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))

        assert response_body["id"] == int(entrylist[0])
        assert response_body["userid"] == entrylist[1]
        assert response_body["filename"] == int(entrylist[2])
        assert response_body["prediction"] == str(entrylist[3])

# Test delete API


@pytest.mark.parametrize("ind", [1, 2])
def test_deleteAPI(client, ind, capsys):
    with capsys.disabled():
        response = client.get(f'/api/delete/{ind}')
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["result"] == "ok"

# Test getall API


def test_getAllAPI(client, capsys):
    with capsys.disabled():
        response = client.get(f'/api/getall')
        ret = json.loads(response.get_data(as_text=True))

        # check the outcome of the auction
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        response_body = json.loads(response.get_data(as_text=True))
        print('Type of response_body: ', type(response_body))
        print('Get all entries: ', response_body)


    entrylist = [[4, 'strawb.png', 'fresh strawberry'],
             [5, 'orange.png', 'fresh orange']]
    assert response_body[0]['id'] == entrylist[0][0]
    assert response_body[1]['id'] == entrylist[1][0]

# Test predict API


@pytest.mark.parametrize("entrylist", [
    [1, 'lulu.png'],
    [1500.0, 500.0, 450.0, 350.0, 9, 2, 0, 2, 8, 10.0, 1, 1, 1, 0, 1, 13, 1]
])
def test_predict(client, entrylist, capsys):
    with capsys.disabled():
        data1 = {'userid': entrylist[0],
                 'filename': entrylist[1]}

    response = client.post('/api/predict',
                           data=json.dumps(data1),
                           content_type="application/json",)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert response_body["results"]

# ==================================================================================

# TESTING FOR USER CLASS

# test get all users API


def test_getAllUsersAPI(client, capsys):
    with capsys.disabled():
        response = client.get(f'/api/getallusers')
        ret = json.loads(response.get_data(as_text=True))

        # check the outcome of the auction
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        response_body = json.loads(response.get_data(as_text=True))
        print('Type of response_body: ', type(response_body))
        print('Get all entries: ', response_body)

        entrylist = [[2, 'jenny@mail.com', 'nicenice'],
                     [3, 'johny@abc.com', 'abcd123']]
        assert response_body[0]['id'] == entrylist[0][0]
        assert response_body[1]['id'] == entrylist[1][0]

# Test get users API


@pytest.mark.parametrize("entrylist", [[2, 'jenny@mail.com', 'nicenice'],
                                       [3, 'johny@abc.com', 'abcd123']])
def test_getUserAPI(client, entrylist, capsys):
    with capsys.disabled():
        response = client.get(f'/api/getUser/{entrylist[0]}')
        ret = json.loads(response.get_data(as_text=True))
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))

        # print('================',entrylist)
        assert response_body["id"] == int(entrylist[0])
        assert response_body["email"] == str(entrylist[1])
        assert response_body["password"] == str(entrylist[2])

# Test add user API


@pytest.mark.parametrize("entrylist", [
    ['jimmy@kmail.com', 'niceguy'],
    ['jason@edf.com', 'veryniceguy']
])
def test_addUserAPI(client, entrylist, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        data1 = {'email': entrylist[0],
                 'password': entrylist[1]}

        # use client object  to post
        # data is converted to json
        # posting content is specified
        response = client.post('/api/addUser',
                               data=json.dumps(data1),
                               content_type="application/json",)
        # check the outcome of the action
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]

# Unit Test
# 2: Parametrize section contains the data for the test


@pytest.mark.parametrize("entrylist", [
    ['james@bond.com', 'goodguy'],  # Test integer arguments
    ['jane@mail.com', 'goodgirl']  # Test float arguments
])
# 3: Write the test function pass in the arguments
def test_UserClass(entrylist, capsys):
    with capsys.disabled():
        print(entrylist)
        new_entry = User(email=entrylist[0],
                         password=entrylist[1])

        assert len(new_entry.email) <= 30
        assert len(new_entry.password) >= 6


@pytest.mark.xfail(reason="arguments <= 0")
@pytest.mark.parametrize("entrylist", [
    ['jamie@fgh.com', 'abcd1234'],
    ['javier@kgh.com', 'noiceee']
])

def test_UserValidation(entrylist,capsys):
    test_UserClass(entrylist,capsys)