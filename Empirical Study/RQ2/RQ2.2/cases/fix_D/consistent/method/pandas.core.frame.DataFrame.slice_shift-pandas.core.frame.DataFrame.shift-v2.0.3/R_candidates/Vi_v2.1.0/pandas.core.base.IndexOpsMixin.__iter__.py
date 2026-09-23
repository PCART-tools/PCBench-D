    def __iter__(self) -> Iterator:
        """
        Return an iterator of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period)

        Returns
        -------
        iterator

        Examples
        --------
        >>> s = pd.Series([1, 2, 3])
        >>> for x in s:
        ...     print(x)
        1
        2
        3
        """
        # We are explicitly making element iterators.
        if not isinstance(self._values, np.ndarray):
            # Check type instead of dtype to catch DTA/TDA
            return iter(self._values)
        else:
            return map(self._values.item, range(self._values.size))
