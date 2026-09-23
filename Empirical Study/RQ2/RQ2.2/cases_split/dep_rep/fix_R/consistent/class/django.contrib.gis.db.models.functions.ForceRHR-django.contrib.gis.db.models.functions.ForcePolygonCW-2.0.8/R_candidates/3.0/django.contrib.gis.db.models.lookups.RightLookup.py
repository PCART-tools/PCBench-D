@BaseSpatialField.register_lookup
class RightLookup(GISLookup):
    """
    The 'right' operator returns true if A's bounding box is strictly to the right
    of B's bounding box.
    """
    lookup_name = 'right'
