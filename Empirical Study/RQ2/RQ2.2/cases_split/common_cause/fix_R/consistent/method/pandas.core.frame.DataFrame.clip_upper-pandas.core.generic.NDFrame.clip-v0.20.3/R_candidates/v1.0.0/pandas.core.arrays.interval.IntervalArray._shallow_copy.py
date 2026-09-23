    def _shallow_copy(self, left=None, right=None, closed=None):
        """
        Return a new IntervalArray with the replacement attributes

        Parameters
        ----------
        left : array-like
            Values to be used for the left-side of the the intervals.
            If None, the existing left and right values will be used.

        right : array-like
            Values to be used for the right-side of the the intervals.
            If None and left is IntervalArray-like, the left and right
            of the IntervalArray-like will be used.

        closed : {'left', 'right', 'both', 'neither'}, optional
            Whether the intervals are closed on the left-side, right-side, both
            or neither.  If None, the existing closed will be used.
        """
        if left is None:

            # no values passed
            left, right = self.left, self.right

        elif right is None:

            # only single value passed, could be an IntervalArray
            # or array of Intervals
            if not isinstance(left, (type(self), ABCIntervalIndex)):
                left = type(self)(left)

            left, right = left.left, left.right
        else:

            # both left and right are values
            pass

        closed = closed or self.closed
        return self._simple_new(left, right, closed=closed, verify_integrity=False)
