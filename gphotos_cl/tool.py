import argparse
from xml.etree import ElementTree

from google_auth_oauthlib.flow import InstalledAppFlow

def get_session(client_secrets, scope):
    flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets,
            scopes=[scope]
    )
    flow.run_local_server()
    return flow.authorized_session()


gphotos_scope = "https://picasaweb.google.com/data/"
url_albums = 'https://picasaweb.google.com/data/feed/api/user/default'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('client_secrets')
    args = parser.parse_args()

    session = get_session(args.client_secrets, gphotos_scope)
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
        print("{}\t{}".format(title, url))

if __name__ == '__main__':
    main()
