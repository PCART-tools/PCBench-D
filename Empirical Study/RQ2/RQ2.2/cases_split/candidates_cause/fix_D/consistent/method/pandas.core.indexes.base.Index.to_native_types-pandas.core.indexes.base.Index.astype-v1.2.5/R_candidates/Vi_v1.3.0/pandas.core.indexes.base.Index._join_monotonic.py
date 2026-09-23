    @final
    def _join_monotonic(self, other: Index, how: str_t = "left"):
        # We only get here with matching dtypes
        assert other.dtype == self.dtype

        if self.equals(other):
            ret_index = other if how == "right" else self
            return ret_index, None, None

        ridx: np.ndarray | None
        lidx: np.ndarray | None

        if self.is_unique and other.is_unique:
            # We can perform much better than the general case
            if how == "left":
                join_index = self
                lidx = None
                ridx = self._left_indexer_unique(other)
            elif how == "right":
                join_index = other
                lidx = other._left_indexer_unique(self)
                ridx = None
            elif how == "inner":
                join_array, lidx, ridx = self._inner_indexer(other)
                join_index = self._wrap_joined_index(join_array, other)
            elif how == "outer":
                join_array, lidx, ridx = self._outer_indexer(other)
                join_index = self._wrap_joined_index(join_array, other)
        else:
            if how == "left":
                join_array, lidx, ridx = self._left_indexer(other)
            elif how == "right":
                join_array, ridx, lidx = other._left_indexer(self)
            elif how == "inner":
                join_array, lidx, ridx = self._inner_indexer(other)
            elif how == "outer":
                join_array, lidx, ridx = self._outer_indexer(other)

            join_index = self._wrap_joined_index(join_array, other)

        lidx = None if lidx is None else ensure_platform_int(lidx)
        ridx = None if ridx is None else ensure_platform_int(ridx)
        return join_index, lidx, ridx
