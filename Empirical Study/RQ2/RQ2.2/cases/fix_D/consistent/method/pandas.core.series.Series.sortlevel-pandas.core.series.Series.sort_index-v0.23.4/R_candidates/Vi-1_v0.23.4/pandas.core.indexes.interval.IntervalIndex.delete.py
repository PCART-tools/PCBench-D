    def delete(self, loc):
        """
        Return a new IntervalIndex with passed location(-s) deleted

        Returns
        -------
        new_index : IntervalIndex
        """
        new_left = self.left.delete(loc)
        new_right = self.right.delete(loc)
        return self._shallow_copy(new_left, new_right)
