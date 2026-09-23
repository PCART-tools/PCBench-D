    def _try_fill(self, value):
        """ if we are a NaT, return the actual fill value """
        if isinstance(value, type(tslib.NaT)) or np.array(isnull(value)).all():
            value = tslib.iNaT
        elif isinstance(value, np.timedelta64):
            pass
        elif com.is_integer(value):
            # coerce to seconds of timedelta
            value = np.timedelta64(int(value * 1e9))
        elif isinstance(value, timedelta):
            value = np.timedelta64(value)

        return value
