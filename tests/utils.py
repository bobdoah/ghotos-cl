from contextlib import contextmanager

import json
import pytest

from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

def populate_authorized_user_file():
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

def raises(error):
    """Wrapper around pytest.raises to support None."""
    if error:
        return pytest.raises(error)
    else:
        @contextmanager
        def not_raises():
            try:
                yield
            except Exception as e:
                raise e
        return not_raises()
