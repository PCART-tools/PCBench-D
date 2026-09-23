    def __array__(self, dtype=None):
        """
        Return the values as a NumPy array.

        Users should not call this directly. Rather, it is invoked by
        :func:`numpy.array` and :func:`numpy.asarray`.

        Parameters
        ----------
        dtype : str or numpy.dtype, optional
            The dtype to use for the resulting NumPy array. By default,
            the dtype is inferred from the data.

        Returns
        -------
        numpy.ndarray
            The values in the series converted to a :class:`numpy.ndarary`
            with the specified `dtype`.

        See Also
        --------
        pandas.array : Create a new array from data.
        Series.array : Zero-copy view to the array backing the Series.
        Series.to_numpy : Series method for similar behavior.

        Examples
        --------
        >>> ser = pd.Series([1, 2, 3])
        >>> np.asarray(ser)
        array([1, 2, 3])

        For timezone-aware data, the timezones may be retained with
        ``dtype='object'``

        >>> tzser = pd.Series(pd.date_range('2000', periods=2, tz="CET"))
        >>> np.asarray(tzser, dtype="object")
        array([Timestamp('2000-01-01 00:00:00+0100', tz='CET', freq='D'),
               Timestamp('2000-01-02 00:00:00+0100', tz='CET', freq='D')],
              dtype=object)

        Or the values may be localized to UTC and the tzinfo discared with
        ``dtype='datetime64[ns]'``

        >>> np.asarray(tzser, dtype="datetime64[ns]")  # doctest: +ELLIPSIS
        array(['1999-12-31T23:00:00.000000000', ...],
              dtype='datetime64[ns]')
        """
        if (dtype is None and isinstance(self.array, ABCDatetimeArray)
                and getattr(self.dtype, 'tz', None)):
            msg = (
                "Converting timezone-aware DatetimeArray to timezone-naive "
                "ndarray with 'datetime64[ns]' dtype. In the future, this "
                "will return an ndarray with 'object' dtype where each "
                "element is a 'pandas.Timestamp' with the correct 'tz'.\n\t"
                "To accept the future behavior, pass 'dtype=object'.\n\t"
                "To keep the old behavior, pass 'dtype=\"datetime64[ns]\"'."
            )
            warnings.warn(msg, FutureWarning, stacklevel=3)
            dtype = 'M8[ns]'
        return np.asarray(self.array, dtype)
