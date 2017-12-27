import pytest

import requests
import requests_mock

@pytest.fixture
def requests_mocker():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def session():
    s = requests.Session()
    yield s
