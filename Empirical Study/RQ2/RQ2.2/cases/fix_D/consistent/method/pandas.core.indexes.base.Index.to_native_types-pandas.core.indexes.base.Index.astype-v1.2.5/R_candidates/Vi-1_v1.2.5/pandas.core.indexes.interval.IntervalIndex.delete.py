    def delete(self, loc):
        """
        Return a new IntervalIndex with passed location(-s) deleted

        Returns
        -------
        IntervalIndex
        """
        new_left = self.left.delete(loc)
        new_right = self.right.delete(loc)
        result = self._data._shallow_copy(new_left, new_right)
        return type(self)._simple_new(result, name=self.name)
