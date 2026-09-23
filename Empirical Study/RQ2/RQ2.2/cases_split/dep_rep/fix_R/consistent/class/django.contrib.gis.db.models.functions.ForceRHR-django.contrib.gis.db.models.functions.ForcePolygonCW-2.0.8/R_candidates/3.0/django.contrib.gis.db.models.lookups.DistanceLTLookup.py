@BaseSpatialField.register_lookup
class DistanceLTLookup(DistanceLookupFromFunction):
    lookup_name = 'distance_lt'
    op = '<'
