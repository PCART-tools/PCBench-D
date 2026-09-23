    def __array__(self, dtype=None):
        if (
            dtype is None
            and isinstance(self._data, DatetimeArray)
            and getattr(self.dtype, "tz", None)
        ):
            msg = (
                "Converting timezone-aware DatetimeArray to timezone-naive "
                "ndarray with 'datetime64[ns]' dtype. In the future, this "
                "will return an ndarray with 'object' dtype where each "
                "element is a 'pandas.Timestamp' with the correct 'tz'.\n\t"
                "To accept the future behavior, pass 'dtype=object'.\n\t"
                "To keep the old behavior, pass 'dtype=\"datetime64[ns]\"'."
            )
            warnings.warn(msg, FutureWarning, stacklevel=3)
            dtype = "M8[ns]"
        return np.asarray(self._data, dtype=dtype)
