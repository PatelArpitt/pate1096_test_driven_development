# src/tests/test_users.py
import json
# from src import db
from src.api.models import User

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'john',
            'email': 'john@algonquincollege.com'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'john@algonquincollege.com was added!' in data['message']

def test_single_user(test_app, test_database):
    user = User(username='jeffrey', email='jeffrey@testdriven.io')
    db.session.add(user)
    db.session.commit()
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'jeffrey' in data['username']
    assert 'jeffrey@testdriven.io' in data['email']

def test_single_user(test_app, test_database, add_user):
    user = add_user('jeffrey', 'jeffrey@testdriven.io')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'jeffrey' in data['username']
    assert 'jeffrey@testdriven.io' in data['email']

def test_delete_user(test_app, test_database, add_user):
    user = add_user('john', 'john@algonquincollege.com')
    client = test_app.test_client()
    resp = client.delete(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert f'{user.email} was removed!' in data['message']


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()  # new
    add_user('john', ' john@algonquincollege.com')
    add_user('fletcher', 'fletcher@notreal.com')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'john' in data[0]['username']
    assert 'john@algonquincollege.com' in data[0]['email']
    assert 'fletcher' in data[1]['username']
    assert 'fletcher@notreal.com' in data[1]['email']

# function to UPDATE user
def test_update_user(test_app, test_database, add_user):
    # create a username with name as 'arpit' and email as 'arpit@algonquincollege.com'
    user = add_user('arpit', 'arpit@algonquincollege.com')
    
    # setting up a client using function 'test_client'
    client = test_app.test_client()

    # creating a PUT request to update user's userrname to 'Arpit123' and email to 'arpit@gmail.com'
    resp = client.put(
        f'/users/{user.id}',
        data = json.dumps({
            'username': 'Arpit123',
            'email': 'arpit@gmail.com'
        }),
        content_type='application/json',
    )

    # parse the response data
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200, f'The email of the user updated to {data["email"]}. The username of the user has been updated to {data["username"]}' in data.get('message')