import argparse

from xml.etree import ElementTree

url_albums = 'https://picasaweb.google.com/data/feed/api/user/default'

from .authorized_session import get_session_from_args

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-secrets')
    parser.add_argument('--authorized-user-file')
    parser.add_argument('--headless', default=False, action="store_true")
    args = parser.parse_args()

    session = get_session_from_args(args)
    response = session.get(url_albums)

    feed = ElementTree.fromstring(response.content)

    albums = {}
    for entry in feed.iter('{http://www.w3.org/2005/Atom}entry'):
        album_title = entry.find('{http://www.w3.org/2005/Atom}title')
        album_id = entry.find('{http://www.w3.org/2005/Atom}id')
        assert album_title is not None 
        assert album_id is not None
        albums[album_title.text] = album_id.text

    for title, url in albums.iteritems():
        print("{}\t{}".format(unicode(title), url))

if __name__ == '__main__':
    main()
