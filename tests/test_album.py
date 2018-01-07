import asciitable
import pytest

import gphotos_cl.album
from gphotos_cl.album import parse_album, get_album, GOOGLE_PICASAWEB_ALBUM_URL
from gphotos_cl.albums import GOOGLE_PICASAWEB_ALBUMS_URL
from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

from utils import populate_authorized_user_file

@pytest.fixture
def albums_data(album_id):
    return """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
    xmlns:gphoto='http://schemas.google.com/photos/2007'
    xmlns:gd='http://schemas.google.com/g/2005'>
  <entry>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID</id>
    <title>Shutup 2017</title>
    <summary>getout</summary>
    <gphoto:id>{}</gphoto:id>
  </entry>
</feed>""".format(album_id)

@pytest.fixture
def album_data():
    return """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:gphoto='http://schemas.google.com/photos/2007'>
	<title type='text'>Shutup 2017</title>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067637794979490</id>
		<title type='text'>DSC04250.JPG</title>
		<gphoto:id>1234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067620880446066</id>
		<title type='text'>DSC04251.JPG</title>
		<gphoto:id>01234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067604173028546</id>
		<title type='text'>DSC04252.JPG</title>
		<gphoto:id>11234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067566023033714</id>
		<title type='text'>DSC04253.JPG</title>
		<gphoto:id>21234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067454130019250</id>
		<title type='text'>DSC04254.JPG</title>
		<gphoto:id>31234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067387094526306</id>
		<title type='text'>DSC04255.JPG</title>
		<gphoto:id>41234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067124102787122</id>
		<title type='text'>DSC04256.JPG</title>
		<gphoto:id>51234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067103135036962</id>
		<title type='text'>DSC04257.JPG</title>
		<gphoto:id>61234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067068805252866</id>
		<title type='text'>DSC04258.JPG</title>
		<gphoto:id>71234567890</gphoto:id>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067068805252867</id>
		<title type='text'>DSC04259.JPG</title>
		<gphoto:id>81234567890</gphoto:id>
	</entry>
</feed>
"""
@pytest.fixture
def album_id():
    return "1234567890"

@pytest.fixture
def photo_id():
    return "1234567890"

def check_album(title, photos, photo_id):
    assert title == "Shutup 2017"
    assert len(photos) == 10
    photo = photos[0]
    assert photo['id'] == photo_id
    assert photo['title'] == 'DSC04250.JPG'
    assert photo['url'] == 'https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067637794979490'

def test_parser(album_data, photo_id):
    title, photos = parse_album(album_data)
    check_album(title, photos, photo_id)

def test_get(requests_mocker, album_data, album_id, photo_id, session):
    url = GOOGLE_PICASAWEB_ALBUM_URL.format(album_id=album_id)
    requests_mocker.get(url, text=album_data)
    title, photos = get_album(session, album_id)
    check_album(title, photos, photo_id)

def test_album(mocker, requests_mocker, album_data, albums_data, album_id, refresh_token, session, isolated_cli_runner):
    args = ['Shutup 2017']
    url = GOOGLE_PICASAWEB_ALBUM_URL.format(album_id=album_id)
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    requests_mocker.get(url, text=album_data)
    requests_mocker.post('https://accounts.google.com/o/oauth2/token', text=refresh_token)
    mocker.patch('gphotos_cl.authorized_session.get_session_from_authorized_user_file')
    gphotos_cl.authorized_session.get_session_from_authorized_user_file.return_value = session
    populate_authorized_user_file()
    result = isolated_cli_runner.invoke(gphotos_cl.album.album, args)
    assert result.exit_code == 0
    table = asciitable.read(result.output, Reader=asciitable.FixedWidthTwoLine)

def test_album_only_titles(mocker, requests_mocker, album_data, albums_data, album_id, refresh_token, session, isolated_cli_runner):
    args = ['Shutup 2017', '--only-titles']
    url = GOOGLE_PICASAWEB_ALBUM_URL.format(album_id=album_id)
    requests_mocker.get(GOOGLE_PICASAWEB_ALBUMS_URL, text=albums_data)
    requests_mocker.get(url, text=album_data)
    requests_mocker.post('https://accounts.google.com/o/oauth2/token', text=refresh_token)
    mocker.patch('gphotos_cl.authorized_session.get_session_from_authorized_user_file')
    gphotos_cl.authorized_session.get_session_from_authorized_user_file.return_value = session
    populate_authorized_user_file()
    result = isolated_cli_runner.invoke(gphotos_cl.album.album, args)
    assert result.exit_code == 0
    titles = result.output.split('\n')
    assert 'DSC04250.JPG' in titles
