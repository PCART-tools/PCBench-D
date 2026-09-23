@BaseSpatialField.register_lookup
class BBContainsLookup(GISLookup):
    """
    The 'bbcontains' operator returns true if A's bounding box completely contains
    by B's bounding box.
    """
    lookup_name = 'bbcontains'
