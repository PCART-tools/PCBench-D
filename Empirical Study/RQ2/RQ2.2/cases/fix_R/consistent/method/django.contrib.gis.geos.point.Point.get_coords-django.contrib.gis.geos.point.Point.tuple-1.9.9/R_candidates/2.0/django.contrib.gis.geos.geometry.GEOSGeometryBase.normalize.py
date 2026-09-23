    def normalize(self):
        "Convert this Geometry to normal form (or canonical form)."
        capi.geos_normalize(self.ptr)
