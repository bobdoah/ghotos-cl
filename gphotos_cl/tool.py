import click

import album
import albums
import authorized_session 


@click.group()
def entrypoint():
    pass

entrypoint.add_command(album.album)
entrypoint.add_command(albums.albums)
entrypoint.add_command(authorized_session.authorize)
