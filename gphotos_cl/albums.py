from xml.etree import ElementTree

from .namespace import GPHOTO_XML_NS

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


