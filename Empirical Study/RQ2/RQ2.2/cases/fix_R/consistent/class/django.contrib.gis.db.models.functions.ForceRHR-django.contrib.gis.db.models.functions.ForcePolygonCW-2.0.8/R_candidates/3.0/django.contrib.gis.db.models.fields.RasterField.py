class RasterField(BaseSpatialField):
    """
    Raster field for GeoDjango -- evaluates into GDALRaster objects.
    """

    description = _("Raster Field")
    geom_type = 'RASTER'
    geography = False

    def _check_connection(self, connection):
        # Make sure raster fields are used only on backends with raster support.
        if not connection.features.gis_enabled or not connection.features.supports_raster:
            raise ImproperlyConfigured('Raster fields require backends with raster support.')

    def db_type(self, connection):
        self._check_connection(connection)
        return super().db_type(connection)

    def from_db_value(self, value, expression, connection):
        return connection.ops.parse_raster(value)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        # Setup for lazy-instantiated Raster object. For large querysets, the
        # instantiation of all GDALRasters can potentially be expensive. This
        # delays the instantiation of the objects to the moment of evaluation
        # of the raster attribute.
        setattr(cls, self.attname, SpatialProxy(gdal.GDALRaster, self))

    def get_transform(self, name):
        from django.contrib.gis.db.models.lookups import RasterBandTransform
        try:
            band_index = int(name)
            return type(
                'SpecificRasterBandTransform',
                (RasterBandTransform,),
                {'band_index': band_index}
            )
        except ValueError:
            pass
        return super().get_transform(name)
