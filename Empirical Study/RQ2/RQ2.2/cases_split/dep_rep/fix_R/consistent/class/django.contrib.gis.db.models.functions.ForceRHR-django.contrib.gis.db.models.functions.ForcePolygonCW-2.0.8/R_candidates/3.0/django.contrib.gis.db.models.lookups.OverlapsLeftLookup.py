@BaseSpatialField.register_lookup
class OverlapsLeftLookup(GISLookup):
    """
    The overlaps_left operator returns true if A's bounding box overlaps or is to the
    left of B's bounding box.
    """
    lookup_name = 'overlaps_left'
