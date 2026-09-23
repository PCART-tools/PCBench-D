    def _try_fill(self, value):
        """ if we are a NaT, return the actual fill value """
        if isinstance(value, type(tslib.NaT)) or np.array(isnull(value)).all():
            value = tslib.iNaT
        return value
