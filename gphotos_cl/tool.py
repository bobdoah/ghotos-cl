import click

import gphotos_cl.album
import gphotos_cl.albums
import gphotos_cl.authorized_session 


@click.group()
def entrypoint():
    pass

entrypoint.add_command(gphotos_cl.album.album)
entrypoint.add_command(gphotos_cl.albums.albums)
entrypoint.add_command(gphotos_cl.authorized_session.authorize)
