import os
import pytest
from movie_app import create_app


TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'Home', 'Documents', 'GitHub', 'CS235Flix-part-2', 'tests', 'data')


@pytest.fixture
def in_memory_repo():
    pass


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                    # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,   # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False           # test_client will not send a CSRF token, so disable validation.
    })
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='clam341', password='justapassword'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
