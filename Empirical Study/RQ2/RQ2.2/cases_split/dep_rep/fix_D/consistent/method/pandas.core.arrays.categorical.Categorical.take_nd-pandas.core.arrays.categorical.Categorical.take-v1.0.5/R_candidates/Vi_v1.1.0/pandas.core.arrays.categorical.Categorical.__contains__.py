    def __contains__(self, key) -> bool:
        """
        Returns True if `key` is in this Categorical.
        """
        # if key is a NaN, check if any NaN is in self.
        if is_valid_nat_for_dtype(key, self.categories.dtype):
            return self.isna().any()

        return contains(self, key, container=self._codes)
