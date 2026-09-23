    @property
    def length(self):
        """
        Return an Index with entries denoting the length of each Interval in
        the IntervalArray.
        """
        try:
            return self.right - self.left
        except TypeError:
            # length not defined for some types, e.g. string
            msg = (
                "IntervalArray contains Intervals without defined length, "
                "e.g. Intervals with string endpoints"
            )
            raise TypeError(msg)
