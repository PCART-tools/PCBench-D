    @cache_readonly
    def _na_value(self):
        """The expected NA value to use with this index."""
        dtype = self.dtype
        if isinstance(dtype, np.dtype):
            if dtype.kind in ["m", "M"]:
                return NaT
            return np.nan
        return dtype.na_value
