    def __getitem__(self, value):
        mask = self._isnan[value]
        if is_scalar(mask) and mask:
            return self._na_value

        left = self.left[value]
        right = self.right[value]

        # scalar
        if not isinstance(left, Index):
            return Interval(left, right, self.closed)

        return self._shallow_copy(left, right)
