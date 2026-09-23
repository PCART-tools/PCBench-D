    def _wrap_joined_index(self, joined: np.ndarray, other):
        assert other.dtype == self.dtype, (other.dtype, self.dtype)

        result = super()._wrap_joined_index(joined, other)
        result._data._freq = self._get_join_freq(other)
        return result
