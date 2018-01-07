import asciitable
import pytest

import gphotos_cl.albums
from gphotos_cl.albums import (
        GOOGLE_PICASAWEB_ALBUMS_URL,
        AlbumNotFound,
        get_albums, 
        get_album_id_by_title, 
        parse_albums
)
from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

from utils import populate_authorized_user_file, raises

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


def check_albums(albums):
    assert albums is not None
    assert len(albums) == 4 
    album = albums[0]
    assert album['title'] == 'lolcats'
    assert album['summary'] == 'Hilarious Felines'
    assert album['url'] == 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID'
    assert album['album_type'] is None
    assert album['id'] == 'albumID'

def test_parser(albums_data):
    albums = parse_albums(albums_data)
    check_albums(albums)

def test_get(requests_mocker, albums_data, session):
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    albums = get_albums(session)
    check_albums(albums)

@pytest.mark.parametrize('title,expected_error,album_id', [
        ("lolcats", None, "albumID"),
        ("nocats", AlbumNotFound, "")
])
def test_get_albumd_id_by_title(requests_mocker, albums_data, session, 
    title, expected_error, album_id):
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    with raises(expected_error):
        assert get_album_id_by_title(session, title) == album_id

@pytest.mark.parametrize('args,url,summary,album_type,title,album_id', [
    ([], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID', 'Hilarious Felines', '', 'lolcats', 'albumID' ),
    (['--no-filter-buzz'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/Buzz', '', 'Buzz', '27/03/2015', 'Buzz' ),
    (['--no-filter-hangout'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/hangout', '', '', 'Hangout: blah', 'hangout' ),
    (['--no-filter-archive'], 'https://picasaweb.google.com/data/entry/api/user/liz/albumid/archive', '', '', '2017-01-20', 'archive' )
    ])
def test_albums(mocker, requests_mocker, albums_data, refresh_token, session, isolated_cli_runner, 
        args, url, summary, album_type, title, album_id):
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    requests_mocker.post('https://accounts.google.com/o/oauth2/token', text=refresh_token)
    mocker.patch('gphotos_cl.authorized_session.get_session_from_authorized_user_file')
    gphotos_cl.authorized_session.get_session_from_authorized_user_file.return_value = session
    populate_authorized_user_file()
    result = isolated_cli_runner.invoke(gphotos_cl.albums.albums, args)
    assert result.exit_code == 0
    table = asciitable.read(result.output, Reader=asciitable.FixedWidthTwoLine)
    assert url in table['url']
    assert summary in table['summary']
    assert album_type in table['album_type']
    assert title in table['title']
    assert album_id in table['id']
    
