    def __array_finalize__(self, obj):
        self.units = getattr(obj, "units", None)
