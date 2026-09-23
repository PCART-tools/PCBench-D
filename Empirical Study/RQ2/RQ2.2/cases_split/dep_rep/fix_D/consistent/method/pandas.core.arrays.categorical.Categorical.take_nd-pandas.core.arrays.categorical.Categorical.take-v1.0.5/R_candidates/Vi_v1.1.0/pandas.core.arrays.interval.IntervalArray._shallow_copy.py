    def _shallow_copy(self, left, right):
        """
        Return a new IntervalArray with the replacement attributes

        Parameters
        ----------
        left : Index
            Values to be used for the left-side of the intervals.
        right : Index
            Values to be used for the right-side of the intervals.
        """
        return self._simple_new(left, right, closed=self.closed, verify_integrity=False)
