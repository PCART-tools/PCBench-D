    @property
    def _internal_fill_value(self) -> int:
        # using the specific numpy integer instead of python int to get
        #  the correct dtype back from _quantile in the all-NA case
        dtype = self._ndarray.dtype
        return dtype.type(-1)
