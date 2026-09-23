    def write(self, geom):
        "Return the WKB representation of the given geometry."
        from django.contrib.gis.geos import Polygon
        geom = self._handle_empty_point(geom)
        wkb = wkb_writer_write(self.ptr, geom.ptr, byref(c_size_t()))
        if isinstance(geom, Polygon) and geom.empty:
            # Fix GEOS output for empty polygon.
            # See https://trac.osgeo.org/geos/ticket/680.
            wkb = wkb[:-8] + b'\0' * 4
        return memoryview(wkb)
