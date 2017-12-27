from xml.etree import ElementTree

import click
import tabulate

from .authorized_session import get_session_from_authorized_user_file, GOOGLE_AUTHORIZED_USER_FILE
from .namespace import GPHOTO_XML_NS

GOOGLE_PICASAWEB_ALBUMS_URL = 'https://picasaweb.google.com/data/feed/api/user/default'

def parse_albums(xml_content):
    albums = {}
    feed = ElementTree.fromstring(xml_content)
    for entry in feed.iterfind('atom:entry', namespaces=GPHOTO_XML_NS):
        album_id = entry.find('gphoto:id', namespaces=GPHOTO_XML_NS)
        album_title = entry.find('atom:title', namespaces=GPHOTO_XML_NS)
        album_url = entry.find('atom:id', namespaces=GPHOTO_XML_NS)
        album_summary = entry.find('atom:summary', namespaces=GPHOTO_XML_NS)
        assert album_title is not None
        assert album_id is not None
        assert album_summary is not None
        assert album_url is not None
        albums[album_id.text] = {
                'title': album_title.text,
                'summary': album_summary.text,
                'url': album_url.text
        }
    return albums

def get_albums(session):
    response = session.get(GOOGLE_PICASAWEB_ALBUMS_URL)
    return parse_albums(response.content)


@click.command()
@click.option('--authorized-user-file', default=GOOGLE_AUTHORIZED_USER_FILE, help="The name of a file to dump the authorized user's token in.", type=click.Path())
def albums(authorized_user_file):
    session = get_session_from_authorized_user_file(authorized_user_file)
    data = {'title':[], 'url':[], 'summary':[]}
    for album_id, album_details in get_albums(session).items():
        data['title'].append(album_details['title'])
        data['url'].append(album_details['url'])
        album_summary = album_details['summary']
        data['summary'].append(album_summary if album_summary is not None else '')
    click.echo(tabulate.tabulate(data, headers='keys'))
