    def cumsum(self, axis, dtype=None):
        """ See da.cumsum for docstring """
        from .reductions import cumsum
        return cumsum(self, axis, dtype)
