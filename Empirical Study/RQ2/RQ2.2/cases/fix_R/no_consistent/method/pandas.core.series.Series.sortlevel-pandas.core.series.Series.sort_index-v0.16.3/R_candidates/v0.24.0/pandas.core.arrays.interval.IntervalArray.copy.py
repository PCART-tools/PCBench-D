    def copy(self, deep=False):
        """
        Return a copy of the array.

        Parameters
        ----------
        deep : bool, default False
            Also copy the underlying data backing this array.

        Returns
        -------
        IntervalArray
        """
        left = self.left.copy(deep=True) if deep else self.left
        right = self.right.copy(deep=True) if deep else self.right
        closed = self.closed
        # TODO: Could skip verify_integrity here.
        return type(self).from_arrays(left, right, closed=closed)
