    def __array__(self, dtype=None):
        # used for Timedelta/DatetimeArray, overwritten by PeriodArray
        if is_object_dtype(dtype):
            return np.array(list(self), dtype=object)
        return self._data
