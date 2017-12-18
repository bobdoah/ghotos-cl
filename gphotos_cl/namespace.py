GPHOTO_XML_NS = { 
    'atom': 'http://www.w3.org/2005/Atom',
    'openSearch': 'http://a9.com/-/spec/opensearch/1.1/',
    'exif': 'http://schemas.google.com/photos/exif/2007',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'gml': 'http://www.opengis.net/gml',
    'georss': 'http://www.georss.org/georss',
    'batch': 'http://schemas.google.com/gdata/batch',
    'media': 'http://search.yahoo.com/mrss/',
    'gphoto': 'http://schemas.google.com/photos/2007',
    'gd': 'http://schemas.google.com/g/2005' 
}
def register_gphoto_namespaces(element_tree):
    for prefix, uri in GPHOTO_XML_NS.items():
        element_tree.register_namespace(prefix, uri)
