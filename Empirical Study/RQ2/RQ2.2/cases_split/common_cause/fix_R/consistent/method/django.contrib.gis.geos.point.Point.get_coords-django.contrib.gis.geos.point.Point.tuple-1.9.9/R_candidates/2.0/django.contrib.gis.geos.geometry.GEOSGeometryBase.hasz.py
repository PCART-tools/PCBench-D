    @property
    def hasz(self):
        "Return whether the geometry has a 3D dimension."
        return capi.geos_hasz(self.ptr)
