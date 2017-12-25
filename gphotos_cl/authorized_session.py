import io
import json
import os.path
import six

import click

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials

GOOGLE_AUTHORIZED_USER_FILE = 'authorized-user.json'

_GOOGLE_OAUTH2_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'

# Hack because current pip-installable doesn't contain this method
def Credentials_from_authorized_user_file(cls, filename, scopes=None):
        with io.open(filename, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        keys_needed = set(('refresh_token', 'client_id', 'client_secret'))
        missing = keys_needed.difference(six.iterkeys(data))
        if missing:
            raise ValueError(
                'Authorized user info was not in the expected format, missing '
                'fields {}.'.format(', '.join(missing)))

        return Credentials(
            None,  # No access token, must be refreshed.
            refresh_token=data['refresh_token'],
            token_uri=_GOOGLE_OAUTH2_TOKEN_ENDPOINT,
            scopes=scopes,
            client_id=data['client_id'],
            client_secret=data['client_secret'])

Credentials.from_authorized_user_file = classmethod(Credentials_from_authorized_user_file)

def get_scopes():
    return "https://picasaweb.google.com/data/"

def get_session_from_client_secrets(client_secrets, headless=False):
    flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets,
            scopes=get_scopes()
    )
    if not headless:
        flow.run_local_server()
    else:
        flow.run_console()
    return flow.authorized_session()

def save_credentials(creds, authorized_user_file):
    with open(authorized_user_file, 'w') as filehandle:
        json.dump({
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }, filehandle)

def load_credentials(authorized_user_file):
    if os.path.exists(authorized_user_file):
        try:
            return Credentials.from_authorized_user_file(authorized_user_file, scopes=get_scopes())
        except ValueError as e:
            print(e)
    return None

@click.command()
@click.argument('client_secrets', type=click.Path(exists=True))
@click.option('--authorized-user-file', default=GOOGLE_AUTHORIZED_USER_FILE, help="The name of a file to dump the authorized user's token in.", type=click.Path())
def auth(client_secrets, authorized_user_file):
    session = get_session_from_client_secrets(client_secrets)
    save_credentials(session, authorized_user_file)
