    def copy(self):
        """
        Return a copy of the array.

        Returns
        -------
        IntervalArray
        """
        left = self.left.copy(deep=True)
        right = self.right.copy(deep=True)
        closed = self.closed
        # TODO: Could skip verify_integrity here.
        return type(self).from_arrays(left, right, closed=closed)
