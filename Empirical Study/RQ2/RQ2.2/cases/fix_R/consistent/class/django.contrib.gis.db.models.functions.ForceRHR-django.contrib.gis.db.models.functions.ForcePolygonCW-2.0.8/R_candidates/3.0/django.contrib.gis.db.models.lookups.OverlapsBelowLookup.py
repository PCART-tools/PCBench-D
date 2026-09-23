@BaseSpatialField.register_lookup
class OverlapsBelowLookup(GISLookup):
    """
    The 'overlaps_below' operator returns true if A's bounding box overlaps or is below
    B's bounding box.
    """
    lookup_name = 'overlaps_below'
