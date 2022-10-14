import json
from src.api.models import User

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post('/users', data=json.dumps({
        'username': 'adam',
        'email': 'adam@email.com',
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'adam@email.com was added!' in data['message']

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_users_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post('/users', data=json.dumps({'email':'adam@email.com'}), content_type='application/json')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_duplication_email(test_app, test_database):
    client = test_app.test_client()
    client.post('/users', data=json.dumps({
        'username': 'adam',
        'email': 'adam@email.com'
        }),
        content_type='application/json',
    )
    resp = client.post('/users', data=json.dumps({
        'username': 'adam',
        'email': 'adam@email.com'
        }),
        content_type='application/json',
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists' in data['message']

def test_single_user(test_app, test_database, add_user):
    user = add_user('adam', 'adam@email.com')
    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'adam' in data['username']
    assert 'adam@email.com' in data['email']

def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get('users/999')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 999 does not exist' in data['message']

def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user('adam', 'adam@email.com')
    add_user('jeff', 'jeff@email.com')
    client = test_app.test_client()
    resp = client.get('/users')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert 'adam' in data[0]['username']
    assert 'jeff' in data[1]['username']
    assert 'adam@email.com' in data[0]['email']
    assert 'jeff@email.com' in data[1]['email']

