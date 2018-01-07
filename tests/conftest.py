import json

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

@pytest.fixture
def authorized_user_file(isolated_cli_runner):
    with open(GOOGLE_AUTHORIZED_USER_FILE, 'w') as f:
        json.dump({
			"_class": "OAuth2Credentials",
			"_module": "oauth2client.client",
			"access_token": "credentials.access_token",
			"client_id": "credentials.client_id",
			"client_secret": "credentials.client_secret",
			"id_token": None,
			"id_token_jwt": None,
			"invalid": False,
			"refresh_token": "credentials.refresh_token",
			"revoke_uri": "https://accounts.google.com/o/oauth2/revoke",
			"scopes": [
				"https://picasaweb.google.com/data/"
			],
			"token_expiry": "2017-12-09T12:34:24Z",
			"token_info_uri": "https://www.googleapis.com/oauth2/v3/tokeninfo",
			"token_response": {
				"access_token": "credentials.access_token",
				"expires_in": 3600,
				"refresh_token": "credentials.refresh_token",
				"token_type": "Bearer"
			},
			"token_uri": "https://accounts.google.com/o/oauth2/token",
			"user_agent": None
		}, f)
        yield f
