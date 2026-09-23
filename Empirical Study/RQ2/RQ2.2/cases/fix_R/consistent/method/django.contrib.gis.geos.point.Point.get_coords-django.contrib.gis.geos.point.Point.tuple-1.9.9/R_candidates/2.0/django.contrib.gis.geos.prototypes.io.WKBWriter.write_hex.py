    def write_hex(self, geom):
        "Return the HEXEWKB representation of the given geometry."
        from django.contrib.gis.geos.polygon import Polygon
        geom = self._handle_empty_point(geom)
        wkb = wkb_writer_write_hex(self.ptr, geom.ptr, byref(c_size_t()))
        if isinstance(geom, Polygon) and geom.empty:
            wkb = wkb[:-16] + b'0' * 8
        return wkb
