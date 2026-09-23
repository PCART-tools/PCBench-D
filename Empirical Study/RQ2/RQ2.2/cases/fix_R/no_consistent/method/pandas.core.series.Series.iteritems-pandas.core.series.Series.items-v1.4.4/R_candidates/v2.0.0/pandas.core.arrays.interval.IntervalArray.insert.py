    def insert(self: IntervalArrayT, loc: int, item: Interval) -> IntervalArrayT:
        """
        Return a new IntervalArray inserting new item at location. Follows
        Python numpy.insert semantics for negative values.  Only Interval
        objects and NA can be inserted into an IntervalIndex

        Parameters
        ----------
        loc : int
        item : Interval

        Returns
        -------
        IntervalArray
        """
        left_insert, right_insert = self._validate_scalar(item)

        new_left = self.left.insert(loc, left_insert)
        new_right = self.right.insert(loc, right_insert)

        return self._shallow_copy(new_left, new_right)
