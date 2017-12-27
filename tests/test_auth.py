import json
import os

import pytest

import gphotos_cl.authorized_session

@pytest.mark.parametrize('headless', [True, False], ids=['console', 'local_server'])
def test_auth(mocker, isolated_cli_runner, headless):
    with open('client_secrets.json', 'w') as f:
       json.dump( 
        {"installed":{
            "client_id":"example.apps.googleusercontent.com",
            "project_id":"example",
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://accounts.google.com/o/oauth2/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":"example",
            "redirect_uris":[
                "urn:ietf:wg:oauth:2.0:oob",
                "http://localhost"
            ]
        }}, f)
    mocker.patch('gphotos_cl.authorized_session.InstalledAppFlow')
    model_spec = {
        'refresh_token': 'credentials.refresh_token',
        'client_id': 'credentials.client_id',
        'client_secret': 'credentials.client_secret',
        'token_uri': 'credentials.token_uri',
        'id_token': 'credentials.id_token',
        'scopes': [list('credentials.scope')], 
        'token': 'credentials.token'
    }
    credentials_mock = mocker.MagicMock()
    credentials_mock.configure_mock(**model_spec)

    gphotos_cl.authorized_session.InstalledAppFlow.from_client_secrets_file.return_value = (gphotos_cl.authorized_session.InstalledAppFlow())
    gphotos_cl.authorized_session.InstalledAppFlow().run_local_server.return_value = credentials_mock
    gphotos_cl.authorized_session.InstalledAppFlow().run_console = credentials_mock
    gphotos_cl.authorized_session.InstalledAppFlow().authorized_session.return_value = credentials_mock
    args = ['client_secrets.json']
    if headless:
        args.append('--headless')
    result = isolated_cli_runner.invoke(gphotos_cl.authorized_session.auth, args)
    assert result.exit_code == 0 
    assert result.output == ''
    assert os.path.exists(gphotos_cl.authorized_session.GOOGLE_AUTHORIZED_USER_FILE)
    gphotos_cl.authorized_session.InstalledAppFlow.from_client_secrets_file.assert_called_once_with(
            'client_secrets.json', scopes=gphotos_cl.authorized_session.get_scopes()
    )
    if headless:
        assert gphotos_cl.authorized_session.InstalledAppFlow().run_console.call_count == 1
    else:
        assert gphotos_cl.authorized_session.InstalledAppFlow().run_local_server.call_count == 1
    assert gphotos_cl.authorized_session.InstalledAppFlow().authorized_session.call_count == 1
