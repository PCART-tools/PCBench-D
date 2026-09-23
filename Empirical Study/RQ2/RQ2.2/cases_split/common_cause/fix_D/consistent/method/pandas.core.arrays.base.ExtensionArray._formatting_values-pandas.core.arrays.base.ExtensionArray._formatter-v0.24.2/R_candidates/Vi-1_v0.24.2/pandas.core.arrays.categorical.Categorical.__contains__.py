    def __contains__(self, key):
        """
        Returns True if `key` is in this Categorical.
        """
        # if key is a NaN, check if any NaN is in self.
        if isna(key):
            return self.isna().any()

        return contains(self, key, container=self._codes)
