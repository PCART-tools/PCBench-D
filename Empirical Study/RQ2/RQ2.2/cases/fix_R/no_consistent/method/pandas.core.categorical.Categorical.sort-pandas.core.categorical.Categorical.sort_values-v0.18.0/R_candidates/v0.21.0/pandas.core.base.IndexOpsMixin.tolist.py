    def tolist(self):
        """
        Return a list of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period)

        See Also
        --------
        numpy.ndarray.tolist
        """

        if is_datetimelike(self):
            return [_maybe_box_datetimelike(x) for x in self._values]
        else:
            return self._values.tolist()
