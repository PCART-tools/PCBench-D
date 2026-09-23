    @property
    def closed(self):
        if geos_version_tuple() < (3, 5):
            raise GEOSException("MultiLineString.closed requires GEOS >= 3.5.0.")
        return super().closed
