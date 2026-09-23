    def _wrap_joined_index(
        self, joined, other, lidx: npt.NDArray[np.intp], ridx: npt.NDArray[np.intp]
    ):
        assert other.dtype == self.dtype, (other.dtype, self.dtype)
        result = super()._wrap_joined_index(joined, other, lidx, ridx)
        result._data._freq = self._get_join_freq(other)
        return result
