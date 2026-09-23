@BaseSpatialField.register_lookup
class DistanceGTELookup(DistanceLookupFromFunction):
    lookup_name = 'distance_gte'
    op = '>='
