    def delete(self: IntervalArrayT, loc) -> IntervalArrayT:
        if isinstance(self._left, np.ndarray):
            new_left = np.delete(self._left, loc)
            new_right = np.delete(self._right, loc)
        else:
            new_left = self._left.delete(loc)
            new_right = self._right.delete(loc)
        return self._shallow_copy(left=new_left, right=new_right)
