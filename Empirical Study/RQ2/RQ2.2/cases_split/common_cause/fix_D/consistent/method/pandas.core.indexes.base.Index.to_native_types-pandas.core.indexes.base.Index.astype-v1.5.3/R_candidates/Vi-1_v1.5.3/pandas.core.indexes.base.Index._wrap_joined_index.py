    def _wrap_joined_index(self: _IndexT, joined: ArrayLike, other: _IndexT) -> _IndexT:
        assert other.dtype == self.dtype

        if isinstance(self, ABCMultiIndex):
            name = self.names if self.names == other.names else None
            # error: Incompatible return value type (got "MultiIndex",
            # expected "_IndexT")
            return self._constructor(joined, name=name)  # type: ignore[return-value]
        else:
            name = get_op_result_name(self, other)
            return self._constructor._with_infer(joined, name=name, dtype=self.dtype)
