from xml.etree import ElementTree

import click

from .authorized_session import get_session_from_authorized_user_file, GOOGLE_AUTHORIZED_USER_FILE
from .namespace import GPHOTO_XML_NS

GOOGLE_PICASAWEB_ALBUM_URL = 'https://picasaweb.google.com/data/feed/api/user/default/albumid/{album_id}?fields=title,entry(title,id)&max-results=10'

def parse_album(xml_content):
    pass

def get_album(session):
    pass
