    @cache_readonly
    def dtype(self):
        """Return the dtype object of the underlying data"""
        return IntervalDtype.construct_from_string(str(self.left.dtype))
