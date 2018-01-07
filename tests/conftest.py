import pytest

import requests
import requests_mock

from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

@pytest.fixture
def requests_mocker():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def session():
    s = requests.Session()
    yield s

@pytest.fixture
def refresh_token():
    return '{ "access_token":"1/fFAGRNJru1FTz70BzhT3Zg", "expires_in":3920, "token_type":"Bearer" }'

