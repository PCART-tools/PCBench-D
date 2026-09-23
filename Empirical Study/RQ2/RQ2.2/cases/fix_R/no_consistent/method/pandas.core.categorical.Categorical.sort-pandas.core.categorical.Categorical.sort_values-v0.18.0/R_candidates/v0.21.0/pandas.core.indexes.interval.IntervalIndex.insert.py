    def insert(self, loc, item):
        if not isinstance(item, Interval):
            raise ValueError('can only insert Interval objects into an '
                             'IntervalIndex')
        if not item.closed == self.closed:
            raise ValueError('inserted item must be closed on the same side '
                             'as the index')
        new_left = self.left.insert(loc, item.left)
        new_right = self.right.insert(loc, item.right)
        return self._shallow_copy(new_left, new_right)
