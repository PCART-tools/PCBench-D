    def __array__(self, dtype: NpDtype | None = None) -> np.ndarray:
        # used for Timedelta/DatetimeArray, overwritten by PeriodArray
        if is_object_dtype(dtype):
            return np.array(list(self), dtype=object)
        return self._ndarray
