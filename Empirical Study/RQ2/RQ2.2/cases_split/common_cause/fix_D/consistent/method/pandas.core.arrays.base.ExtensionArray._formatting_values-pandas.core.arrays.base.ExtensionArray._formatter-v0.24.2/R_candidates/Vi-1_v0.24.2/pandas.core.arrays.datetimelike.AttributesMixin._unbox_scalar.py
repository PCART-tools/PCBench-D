    def _unbox_scalar(self, value):
        # type: (Union[Period, Timestamp, Timedelta, NaTType]) -> int
        """
        Unbox the integer value of a scalar `value`.

        Parameters
        ----------
        value : Union[Period, Timestamp, Timedelta]

        Returns
        -------
        int

        Examples
        --------
        >>> self._unbox_scalar(Timedelta('10s'))  # DOCTEST: +SKIP
        10000000000
        """
        raise AbstractMethodError(self)
