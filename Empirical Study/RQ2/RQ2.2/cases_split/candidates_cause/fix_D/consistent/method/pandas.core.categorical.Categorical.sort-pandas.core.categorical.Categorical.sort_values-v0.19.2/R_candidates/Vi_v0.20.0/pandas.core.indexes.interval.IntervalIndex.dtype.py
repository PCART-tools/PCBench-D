    @cache_readonly
    def dtype(self):
        return IntervalDtype.construct_from_string(str(self.left.dtype))
