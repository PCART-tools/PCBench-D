    def _try_fill(self, value):
        """ if we are a NaT, return the actual fill value """
        if isinstance(value, type(tslib.NaT)) or isnull(value):
            value = tslib.iNaT
        return value
