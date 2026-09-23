class AsteriskPolygonCollection(RegularPolyCollection):
    """Draw a collection of regular asterisks with *numsides* points."""
    _path_generator = mpath.Path.unit_regular_asterisk
