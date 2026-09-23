    def __iter__(self):
        """
        Return an iterator of the values.

        These are each a scalar type, which is a Python scalar
        (for str, int, float) or a pandas scalar
        (for Timestamp/Timedelta/Interval/Period)

        Returns
        -------
        iterator
        """
        # We are explicitly making element iterators.
        if self.dtype.kind in ["m", "M"]:
            return map(com.maybe_box_datetimelike, self._values)
        elif is_extension_array_dtype(self._values):
            return iter(self._values)
        else:
            return map(self._values.item, range(self._values.size))
