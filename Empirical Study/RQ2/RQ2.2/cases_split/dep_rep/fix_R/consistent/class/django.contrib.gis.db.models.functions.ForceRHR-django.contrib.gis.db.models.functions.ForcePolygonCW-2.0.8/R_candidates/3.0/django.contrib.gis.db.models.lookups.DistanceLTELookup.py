@BaseSpatialField.register_lookup
class DistanceLTELookup(DistanceLookupFromFunction):
    lookup_name = 'distance_lte'
    op = '<='
