@BaseSpatialField.register_lookup
class StrictlyBelowLookup(GISLookup):
    """
    The 'strictly_below' operator returns true if A's bounding box is strictly below B's
    bounding box.
    """
    lookup_name = 'strictly_below'
