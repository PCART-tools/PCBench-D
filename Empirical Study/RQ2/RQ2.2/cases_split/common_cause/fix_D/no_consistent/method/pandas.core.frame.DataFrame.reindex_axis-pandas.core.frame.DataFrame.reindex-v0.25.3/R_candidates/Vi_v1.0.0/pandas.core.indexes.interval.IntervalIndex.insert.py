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
        if isinstance(item, Interval):
            if item.closed != self.closed:
                raise ValueError(
                    "inserted item must be closed on the same side as the index"
                )
            left_insert = item.left
            right_insert = item.right
        elif is_scalar(item) and isna(item):
            # GH 18295
            left_insert = right_insert = item
        else:
            raise ValueError(
                "can only insert Interval objects and NA into an IntervalIndex"
            )

        new_left = self.left.insert(loc, left_insert)
        new_right = self.right.insert(loc, right_insert)
        return self._shallow_copy(new_left, new_right)
