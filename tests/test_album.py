import pytest

from gphotos_cl.album import parse_album, get_album, GOOGLE_PICASAWEB_ALBUM_URL
from gphotos_cl.authorized_session import GOOGLE_AUTHORIZED_USER_FILE

@pytest.fixture
def album_data():
    return """<?xml version='1.0' encoding='UTF-8'?>
<feed xmlns='http://www.w3.org/2005/Atom' xmlns:gphoto='http://schemas.google.com/photos/2007'>
	<title type='text'>Shutup 2017</title>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067637794979490</id>
		<title type='text'>DSC04250.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067620880446066</id>
		<title type='text'>DSC04251.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067604173028546</id>
		<title type='text'>DSC04252.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067566023033714</id>
		<title type='text'>DSC04253.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067454130019250</id>
		<title type='text'>DSC04254.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067387094526306</id>
		<title type='text'>DSC04255.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067124102787122</id>
		<title type='text'>DSC04256.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067103135036962</id>
		<title type='text'>DSC04257.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067068805252866</id>
		<title type='text'>DSC04258.JPG</title>
	</entry>
	<entry>
		<id>https://picasaweb.google.com/data/entry/api/user/1234567890/albumid/6481571366544569105/photoid/6482067068805252867</id>
		<title type='text'>DSC04259.JPG</title>
	</entry>
</feed>
"""
def test_parser(album_data):
    albums = parse_album(album_data)

def test_album(mocker, requests_mocker, album_data, refresh_token, session, isolated_cli_runner):
	pass
