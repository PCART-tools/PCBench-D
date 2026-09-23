class GeomOutputGeoFunc(GeoFunc):
    @cached_property
    def output_field(self):
        return GeometryField(srid=self.geo_field.srid)
