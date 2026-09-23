    def _wrap_joined_index(
        self: _IndexT, joined: np.ndarray, other: _IndexT
    ) -> _IndexT:
        assert other.dtype == self.dtype

        if isinstance(self, ABCMultiIndex):
            name = self.names if self.names == other.names else None
        else:
            name = get_op_result_name(self, other)
        return self._constructor(joined, name=name)
