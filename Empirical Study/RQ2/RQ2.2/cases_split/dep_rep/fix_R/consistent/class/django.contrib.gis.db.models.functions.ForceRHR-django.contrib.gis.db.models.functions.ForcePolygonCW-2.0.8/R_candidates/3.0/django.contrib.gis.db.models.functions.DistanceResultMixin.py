class DistanceResultMixin:
    @cached_property
    def output_field(self):
        return DistanceField(self.geo_field)

    def source_is_geography(self):
        return self.geo_field.geography and self.geo_field.srid == 4326
