@BaseSpatialField.register_lookup
class BBOverlapsLookup(GISLookup):
    """
    The 'bboverlaps' operator returns true if A's bounding box overlaps B's bounding box.
    """
    lookup_name = 'bboverlaps'
