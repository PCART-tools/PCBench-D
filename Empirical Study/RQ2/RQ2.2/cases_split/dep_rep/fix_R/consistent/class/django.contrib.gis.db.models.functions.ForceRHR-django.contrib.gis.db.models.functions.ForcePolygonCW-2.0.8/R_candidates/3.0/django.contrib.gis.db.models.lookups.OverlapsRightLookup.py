@BaseSpatialField.register_lookup
class OverlapsRightLookup(GISLookup):
    """
    The 'overlaps_right' operator returns true if A's bounding box overlaps or is to the
    right of B's bounding box.
    """
    lookup_name = 'overlaps_right'
