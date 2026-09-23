    def copy(self: IntervalArrayT) -> IntervalArrayT:
        """
        Return a copy of the array.

        Returns
        -------
        IntervalArray
        """
        left = self._left.copy()
        right = self._right.copy()
        closed = self.closed
        # TODO: Could skip verify_integrity here.
        return type(self).from_arrays(left, right, closed=closed)
