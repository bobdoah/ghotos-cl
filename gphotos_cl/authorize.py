import argparse

from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage


def main():
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('client_secrets')
    args = parser.parse_args()

    scope = "https://picasaweb.google.com/data/"
    flow = flow_from_clientsecrets(args.client_secrets, scope=scope)
    storage = Storage('gphotos_cl.credentials')
    
    credentials = tools.run_flow(flow, storage, args)

if __name__ == '__main__':
    main()
