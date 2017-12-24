import argparse

from xml.etree import ElementTree

url_albums = 'https://picasaweb.google.com/data/feed/api/user/default'

from .authorized_session import get_session_from_args
from .albums import parse_albums

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--client-secrets')
    parser.add_argument('--authorized-user-file')
    parser.add_argument('--headless', default=False, action="store_true")
    args = parser.parse_args()

    session = get_session_from_args(args)
    response = session.get(url_albums)
    albums = parse_albums(response.content)
    print(albums)

if __name__ == '__main__':
    main()
