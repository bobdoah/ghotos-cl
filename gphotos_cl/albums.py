import datetime

from xml.etree import ElementTree

import click
import tabulate

from .authorized_session import get_session_from_authorized_user_file, GOOGLE_AUTHORIZED_USER_FILE
from .namespace import GPHOTO_XML_NS

GOOGLE_PICASAWEB_ALBUMS_URL = 'https://picasaweb.google.com/data/feed/api/user/default?fields=entry(id,gphoto:id,title,summary,gphoto:albumType)'

class AlbumNotFound(Exception):
    pass

def parse_albums(xml_content):
    albums = {}
    feed = ElementTree.fromstring(xml_content)
    for entry in feed.iterfind('atom:entry', namespaces=GPHOTO_XML_NS):
        album_id = entry.find('gphoto:id', namespaces=GPHOTO_XML_NS)
        album_title = entry.find('atom:title', namespaces=GPHOTO_XML_NS)
        album_url = entry.find('atom:id', namespaces=GPHOTO_XML_NS)
        album_summary = entry.find('atom:summary', namespaces=GPHOTO_XML_NS)
        album_type = entry.find('gphoto:albumType', namespaces=GPHOTO_XML_NS)
        if album_type is not None:
            album_type = album_type.text
        assert album_title is not None
        assert album_id is not None
        assert album_summary is not None
        assert album_url is not None
        album_id = album_id.text
        albums[album_id] = {
                'title': album_title.text,
                'summary': album_summary.text,
                'url': album_url.text,
                'album_type':album_type,
                'id':album_id
        }
    return albums

def get_albums(session):
    response = session.get(GOOGLE_PICASAWEB_ALBUMS_URL)
    return parse_albums(response.content)

def get_album_id_by_title(session, album_title):
    for album in get_albums(session).values():
        if album['title'] == album_title:
            return album['id']
    raise AlbumNotFound('album with title {} not found'.format(album_title))

def is_date(album_title):
    try:
        datetime.datetime.strptime(album_title, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@click.command()
@click.option('--authorized-user-file', default=GOOGLE_AUTHORIZED_USER_FILE, help="The name of a file to dump the authorized user's token in.", type=click.Path())
@click.option('--filter-buzz/--no-filter-buzz', default=True, help="Don't show albums from Buzz and Google+")
@click.option('--filter-hangout/--no-filter-hangout', default=True, help="Don't show albums from Hangouts")
@click.option('--filter-archive/--no-filter-archive', default=True, help="Don't show archived albums (date only title)")
def albums(authorized_user_file, filter_buzz, filter_hangout, filter_archive):
    session = get_session_from_authorized_user_file(authorized_user_file)
    data = [['title', 'summary', 'album_type', 'url', 'id']]
    albums = get_albums(session)
    for album_details in sorted(albums.values(), key=lambda k: k['title'].lower()):
        if album_details['album_type'] == 'Buzz' and filter_buzz:
            continue
        if 'Hangout: ' in album_details['title'] and filter_hangout:
            continue 
        if is_date(album_details['title']) and filter_archive:
            continue
        data.append([album_details['title'],
            album_details['summary'],
            album_details['album_type'],
            album_details['url'],
            album_details['id']])
    click.echo(tabulate.tabulate(data, headers='firstrow'))
