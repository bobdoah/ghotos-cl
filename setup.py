from setuptools import setup

setup(
    name='gphotos-cl',
    version='0.1',
    description='Google Photos command line client',
    url='http://github.com/bobdoah/gphotos-cl',
    author='Rob Williams',
    author_email='robertwilliams1985@gmail.com',
    packages=['gphotos_cl'],
    install_requires=[
          'google-auth-oauthlib',
    ]
)
