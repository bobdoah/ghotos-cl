from xml.etree import ElementTree

import click

from .authorized_session import get_session_from_authorized_user_file, GOOGLE_AUTHORIZED_USER_FILE
from .namespace import GPHOTO_XML_NS

GOOGLE_PICASAWEB_ALBUM_URL = 'https://picasaweb.google.com/data/feed/api/user/default/albumid/{album_id}?fields=title,entry(title,id)&max-results=10'

def parse_album(xml_content):
    photos = {}
    feed = ElementTree.fromstring(xml_content)
    title = feed.find('atom:title', namespaces=GPHOTO_XML_NS)
    assert title is not None
    title = title.text
    for entry in feed.iterfind('atom:entry', namespaces=GPHOTO_XML_NS):
        photo_url = entry.find('atom:id', namespaces=GPHOTO_XML_NS)
        photo_title = entry.find('atom:title', namespaces=GPHOTO_XML_NS)
        photo_id = entry.find('gphoto:id', namespaces=GPHOTO_XML_NS)
        assert photo_url is not None
        assert photo_title is not None
        assert photo_id is not None
        photo_id = photo_id.text
        photos[photo_id] = {
            'url': photo_url.text,
            'title':photo_title.text,
            'id':photo_id
        }
    return title, photos

    

def get_album(session, album_id):
    response = session.get(GOOGLE_PICASAWEB_ALBUM_URL.format(album_id=album_id))
    return parse_album(response.content)

@click.command()
@click.option('--authorized-user-file', default=GOOGLE_AUTHORIZED_USER_FILE, help="The name of a file to dump the authorized user's token in.", type=click.Path())
@click.argument('album_name')
def album(album_name, authorized_user_file):
    session = get_session_from_authorized_user_file(authorized_user_file)
    data = [['title', 'url', 'id']]
