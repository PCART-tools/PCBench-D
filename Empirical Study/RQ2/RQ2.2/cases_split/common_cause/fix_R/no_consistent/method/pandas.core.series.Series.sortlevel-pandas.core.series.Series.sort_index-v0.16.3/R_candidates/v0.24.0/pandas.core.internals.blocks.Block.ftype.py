    @property
    def ftype(self):
        if getattr(self.values, '_pandas_ftype', False):
            dtype = self.dtype.subtype
        else:
            dtype = self.dtype
        return "{dtype}:{ftype}".format(dtype=dtype, ftype=self._ftype)
