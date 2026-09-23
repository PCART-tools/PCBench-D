@BaseSpatialField.register_lookup
class ContainedLookup(GISLookup):
    """
    The 'contained' operator returns true if A's bounding box is completely contained
    by B's bounding box.
    """
    lookup_name = 'contained'
