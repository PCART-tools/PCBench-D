    def insert(self, loc, item):
        """
        Return a new IntervalIndex inserting new item at location. Follows
        Python list.append semantics for negative values.  Only Interval
        objects and NA can be inserted into an IntervalIndex

        Parameters
        ----------
        loc : int
        item : object

        Returns
        -------
        IntervalIndex
        """
        left_insert, right_insert = self._data._validate_scalar(item)

        new_left = self.left.insert(loc, left_insert)
        new_right = self.right.insert(loc, right_insert)
        result = self._data._shallow_copy(new_left, new_right)
        return type(self)._simple_new(result, name=self.name)
