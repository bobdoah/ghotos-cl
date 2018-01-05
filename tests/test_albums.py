import json

import asciitable
import pytest

import gphotos_cl.albums
from gphotos_cl.albums import parse_albums, get_albums, GOOGLE_PICASAWEB_ALBUMS_URL
from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

@pytest.fixture
def albums_data():
    return """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
    xmlns:gphoto='http://schemas.google.com/photos/2007'
    xmlns:gd='http://schemas.google.com/g/2005'>
  <entry>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID</id>
    <title>lolcats</title>
    <summary>Hilarious Felines</summary>
    <gphoto:id>albumID</gphoto:id>
  </entry>
  <entry>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/hangout</id>
    <title>Hangout: blah</title>
    <summary></summary>
    <gphoto:id>hangout</gphoto:id>
  </entry>
  <entry>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/Buzz</id>
    <title>27/03/2015</title>
    <summary></summary>
    <gphoto:id>Buzz</gphoto:id>
    <gphoto:albumType>Buzz</gphoto:albumType>
 </entry>
   <entry>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/archive</id>
    <title>2017-01-20</title>
    <summary></summary>
    <gphoto:id>archive</gphoto:id>
  </entry>
</feed>
"""

def test_parser(albums_data):
    albums = parse_albums(albums_data)
    assert ['albumID' in albums]
    album = albums['albumID'] 
    assert album['title'] == 'lolcats'
    assert album['summary'] == 'Hilarious Felines'
    assert album['url'] == 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID'
    assert album['album_type'] is None

def test_get(requests_mocker, albums_data, session):
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    albums = get_albums(session)
    assert albums is not None
    assert ['albumID' in albums]
    album = albums['albumID'] 
    assert album['title'] == 'lolcats'
    assert album['summary'] == 'Hilarious Felines'
    assert album['url'] == 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID'
    assert album['album_type'] is None

@pytest.mark.parametrize('args,url,summary,album_type,title,album_id', [
    [[], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID', 'Hilarious Felines', '', 'lolcats', 'albumID'],
    [['--no-filter-buzz'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/Buzz', '', 'Buzz', '27/03/2015', 'Buzz'],
    [['--no-filter-hangout'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/hangout', '', '', 'Hangout: blah', 'hangout'],
    [['--no-filter-archive'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/archive', '', '', '2017-01-20', 'archive']
    ])
def test_albums(mocker, requests_mocker, albums_data, refresh_token, session, isolated_cli_runner,
        args, url, summary, album_type, title, album_id):
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    requests_mocker.post('https://accounts.google.com/o/oauth2/token', text=refresh_token)
    mocker.patch('gphotos_cl.authorized_session.get_session_from_authorized_user_file')
    gphotos_cl.authorized_session.get_session_from_authorized_user_file.return_value = session
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
    result = isolated_cli_runner.invoke(gphotos_cl.albums.albums, args)
    assert result.exit_code == 0
    table = asciitable.read(result.output, Reader=asciitable.FixedWidthTwoLine)
    assert url in table['url']
    assert summary in table['summary']
    assert album_type in table['album_type']
    assert title in table['title']
    assert album_id in table['id']
    
