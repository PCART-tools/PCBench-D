    def cumprod(self, axis, dtype=None, out=None):
        """ See da.cumprod for docstring """
        from .reductions import cumprod
        return cumprod(self, axis, dtype, out=out)
