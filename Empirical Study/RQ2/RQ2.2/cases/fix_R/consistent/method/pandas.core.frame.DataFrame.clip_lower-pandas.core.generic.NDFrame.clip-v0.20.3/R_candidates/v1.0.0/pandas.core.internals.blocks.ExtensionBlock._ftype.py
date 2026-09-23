    @property
    def _ftype(self):
        return getattr(self.values, "_pandas_ftype", Block._ftype)
