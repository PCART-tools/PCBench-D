    def _unbox_scalar(
        self, value: DTScalarOrNaT, setitem: bool = False
    ) -> np.int64 | np.datetime64 | np.timedelta64:
        """
        Unbox the integer value of a scalar `value`.

        Parameters
        ----------
        value : Period, Timestamp, Timedelta, or NaT
            Depending on subclass.
        setitem : bool, default False
            Whether to check compatibility with setitem strictness.

        Returns
        -------
        int

        Examples
        --------
        >>> self._unbox_scalar(Timedelta("10s"))  # doctest: +SKIP
        10000000000
        """
        raise AbstractMethodError(self)
