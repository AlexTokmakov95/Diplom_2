import pytest
import requests

from data.urls import Urls
from data.user_data import User


@pytest.fixture(scope="function")
def create_user():
    payload = User.create_data_user()
    login_data = payload.copy()
    del login_data["name"]
    response = requests.post(Urls.url_create_user, data=payload)
    token = response.json()["accessToken"]
    yield response, payload, login_data, token
    requests.delete(Urls.url_delete_user, headers={'Authorization': f'{token}'})