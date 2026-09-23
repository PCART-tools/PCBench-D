    def astype(self, dtype: AstypeArg, copy: bool = True) -> ArrayLike:
        """
        Cast to a NumPy array or ExtensionArray with 'dtype'.

        Parameters
        ----------
        dtype : str or dtype
            Typecode or data-type to which the array is cast.
        copy : bool, default True
            Whether to copy the data, even if not necessary. If False,
            a copy is made only if the old dtype does not match the
            new dtype.

        Returns
        -------
        np.ndarray or pandas.api.extensions.ExtensionArray
            An ExtensionArray if dtype is ExtensionDtype,
            Otherwise a NumPy ndarray with 'dtype' for its dtype.
        """

        dtype = pandas_dtype(dtype)
        if is_dtype_equal(dtype, self.dtype):
            if not copy:
                return self
            else:
                return self.copy()

        if isinstance(dtype, ExtensionDtype):
            cls = dtype.construct_array_type()
            return cls._from_sequence(self, dtype=dtype, copy=copy)

        elif is_datetime64_dtype(dtype):
            from pandas.core.arrays import DatetimeArray

            return DatetimeArray._from_sequence(self, dtype=dtype, copy=copy)

        elif is_timedelta64_dtype(dtype):
            from pandas.core.arrays import TimedeltaArray

            return TimedeltaArray._from_sequence(self, dtype=dtype, copy=copy)

        return np.array(self, dtype=dtype, copy=copy)
