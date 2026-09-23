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
        if is_datetimelike(self._values):
            return [com.maybe_box_datetimelike(x) for x in self._values]
        elif is_extension_array_dtype(self._values):
            return list(self._values)
        else:
            return self._values.tolist()
