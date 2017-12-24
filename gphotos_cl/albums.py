from xml.etree import ElementTree

from .namespace import register_gphoto_namespaces

def parse_albums(xml_content):
    register_gphoto_namespaces(ElementTree)
    albums = {}
    feed = ElementTree.fromstring(xml_content)
    import pdb
    pdb.set_trace()
    for entry in feed.iter('atom:entry'):
        album_title = entry.find('atom:title')
        album_id = entry.find('atom:id')
        assert album_title is not None
        assert album_id is not None
        albums[album_id.text] = {
                'title': album_title.text,
                'summary': album_title.summary
        }
    return albums


