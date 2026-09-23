    def __getitem__(self, value):
        left = self.left[value]
        right = self.right[value]

        # scalar
        if not isinstance(left, Index):
            if isna(left):
                return self._fill_value
            return Interval(left, right, self.closed)

        return self._shallow_copy(left, right)
