from test.utils import *
from app.router.user import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'aadarsh4u'
    assert response.json()['email'] == 'derekheart020@gmail.com'
    assert response.json()['first_name'] == 'aadarsh'
    assert response.json()['last_name'] == 'kushwaha'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '2222222222'


def test_change_password_success(test_user):
    response = client.put("/user/password", json={"password": "123456",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/user/password", json={"password": "wrong_password",
                                                  "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password'}


def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT






