@BaseSpatialField.register_lookup
class DistanceGTLookup(DistanceLookupFromFunction):
    lookup_name = 'distance_gt'
    op = '>'
