    def _wrap_joined_index(self, joined: np.ndarray, other):
        assert other.dtype == self.dtype, (other.dtype, self.dtype)
        name = get_op_result_name(self, other)

        freq = self.freq if self._can_fast_union(other) else None
        new_data = type(self._data)._simple_new(  # type: ignore
            joined, dtype=self.dtype, freq=freq
        )

        return type(self)._simple_new(new_data, name=name)
