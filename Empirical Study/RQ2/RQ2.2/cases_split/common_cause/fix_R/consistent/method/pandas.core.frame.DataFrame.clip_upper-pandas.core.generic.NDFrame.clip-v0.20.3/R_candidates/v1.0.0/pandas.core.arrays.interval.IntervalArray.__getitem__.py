    def __getitem__(self, value):
        value = check_array_indexer(self, value)
        left = self.left[value]
        right = self.right[value]

        # scalar
        if not isinstance(left, ABCIndexClass):
            if is_scalar(left) and isna(left):
                return self._fill_value
            if np.ndim(left) > 1:
                # GH#30588 multi-dimensional indexer disallowed
                raise ValueError("multi-dimensional indexing not allowed")
            return Interval(left, right, self.closed)

        return self._shallow_copy(left, right)
