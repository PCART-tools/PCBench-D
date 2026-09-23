    @doc(Index.__contains__)
    def __contains__(self, key: Any) -> bool:
        # if key is a NaN, check if any NaN is in self.
        if is_valid_nat_for_dtype(key, self.categories.dtype):
            return self.hasnans

        return contains(self, key, container=self._engine)
