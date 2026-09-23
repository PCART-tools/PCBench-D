    def cumprod(self, axis, dtype=None):
        """ See da.cumprod for docstring """
        from .reductions import cumprod
        return cumprod(self, axis, dtype)
