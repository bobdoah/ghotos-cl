import pytest

from gphotos_cl.albums import parse_albums

@pytest.fixture
def album_data():
    return """<?xml version='1.0' encoding='utf-8'?>
<feed xmlns='http://www.w3.org/2005/Atom'
    xmlns:openSearch='http://a9.com/-/spec/opensearch/1.1/'
    xmlns:exif='http://schemas.google.com/photos/exif/2007'
    xmlns:geo='http://www.w3.org/2003/01/geo/wgs84_pos#'
    xmlns:gml='http://www.opengis.net/gml'
    xmlns:georss='http://www.georss.org/georss'
    xmlns:batch='http://schemas.google.com/gdata/batch'
    xmlns:media='http://search.yahoo.com/mrss/'
    xmlns:gphoto='http://schemas.google.com/photos/2007'
    xmlns:gd='http://schemas.google.com/g/2005'
    gd:etag='W/"CkABRXY8fip7ImA9WxVVGE8."'>
  <id>https://picasaweb.google.com/data/feed/api/user/liz</id>
  <updated>2009-03-12T01:19:14.876Z</updated>
  <category scheme='http://schemas.google.com/g/2005#kind'
    term='http://schemas.google.com/photos/2007#user' />
  <title>liz</title>
  <subtitle></subtitle>
  <icon>https://iconPath/liz.jpg</icon>
  <link rel='http://schemas.google.com/g/2005#feed'
    type='application/atom+xml'
    href='https://picasaweb.google.com/data/feed/api/user/liz' />
  <link rel='http://schemas.google.com/g/2005#post'
    type='application/atom+xml'
    href='https://picasaweb.google.com/data/feed/api/user/liz' />
  <link rel='alternate' type='text/html'
    href='http://picasaweb.google.com/liz' />
  <link rel='http://schemas.google.com/photos/2007#slideshow'
    type='application/x-shockwave-flash'
    href='http://picasaweb.google.com/s/c/bin/slideshow.swf?host=picasaweb.google.com&amp;RGB=0x000000&amp;feed=https%3A%2F%2Fpicasaweb.google.com%2Fdata%2Ffeed%2Fapi%2Fuser%2Fliz%3Falt%3Drss' />
  <link rel='self' type='application/atom+xml'
    href='https://picasaweb.google.com/data/feed/api/user/liz?start-index=1&amp;max-results=1000&amp;v=2' />
  <author>
    <name>Liz</name>
    <uri>http://picasaweb.google.com/liz</uri>
  </author>
  <generator version='1.00' uri='http://picasaweb.google.com/'>
    Picasaweb</generator>
  <openSearch:totalResults>1</openSearch:totalResults>
  <openSearch:startIndex>1</openSearch:startIndex>
  <openSearch:itemsPerPage>1000</openSearch:itemsPerPage>
  <gphoto:user>liz</gphoto:user>
  <gphoto:nickname>Liz</gphoto:nickname>
  <gphoto:thumbnail>
    https://thumbnailPath/liz.jpg</gphoto:thumbnail>
  <gphoto:quotalimit>1073741824</gphoto:quotalimit>
  <gphoto:quotacurrent>32716</gphoto:quotacurrent>
  <gphoto:maxPhotosPerAlbum>500</gphoto:maxPhotosPerAlbum>
  <entry gd:etag='"RXY8fjVSLyp7ImA9WxVVGE8KQAE."'>
    <id>https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID</id>
    <published>2005-06-17T07:09:42.000Z</published>
    <updated>2009-03-12T01:19:14.000Z</updated>
    <app:edited xmlns:app='http://www.w3.org/2007/app'>
      2009-03-12T01:19:14.000Z</app:edited>
    <category scheme='http://schemas.google.com/g/2005#kind'
      term='http://schemas.google.com/photos/2007#album' />
    <title>lolcats</title>
    <summary>Hilarious Felines</summary>
    <rights>public</rights>
    <link rel='http://schemas.google.com/g/2005#feed'
      type='application/atom+xml'
      href='https://picasaweb.google.com/data/feed/api/user/liz/albumid/albumID?authkey=authKey&amp;v=2' />
    <link rel='alternate' type='text/html'
      href='http://picasaweb.google.com/lh/album/aFDUU2eJpMHZ1dP5TGaYHxtMTjNZETYmyPJy0liipFm0?authkey=authKey' />
    <link rel='self' type='application/atom+xml'
      href='https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID?authkey=authKey&amp;v=2' />
    <link rel='edit' type='application/atom+xml'
      href='https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID/1236820754876000?authkey=authKey&amp;v=2' />
    <link rel='http://schemas.google.com/acl/2007#accessControlList'
      type='application/atom+xml'
      href='https://picasaweb.google.com/data/entry/api/user/liz/albumid/albumID/acl?authkey=authKey&amp;v=2' />
    <author>
      <name>Liz</name>
      <uri>http://picasaweb.google.com/liz</uri>
    </author>
    <gphoto:id>albumID</gphoto:id>
    <gphoto:location>Mountain View, CA</gphoto:location>
    <gphoto:access>public</gphoto:access>
    <gphoto:timestamp>1118992182000</gphoto:timestamp>
    <gphoto:numphotos>1</gphoto:numphotos>
    <gphoto:numphotosremaining>499</gphoto:numphotosremaining>
    <gphoto:bytesUsed>23044</gphoto:bytesUsed>
    <gphoto:user>liz</gphoto:user>
    <gphoto:nickname>Liz</gphoto:nickname>
    <media:group>
      <media:title type='plain'>lolcats</media:title>
      <media:description type='plain'>Hilarious
        Felines</media:description>
      <media:keywords></media:keywords>
      <media:content url='https://imagePath/Lolcats.jpg' type='image/jpeg' medium='image' />
      <media:thumbnail url='https://thumbnailPath/Lolcats.jpg' height='160' width='160' />
      <media:credit>Liz</media:credit>
    </media:group>
  </entry>
</feed>
"""

def test_parser(album_data):
    albums = parse_albums(album_data)
    assert 'albumID' in albums
    album = albums['albumID'] 
    assert album['title'] == 'lolcats'
    assert album['summary'] == 'Hilarious Felines'
