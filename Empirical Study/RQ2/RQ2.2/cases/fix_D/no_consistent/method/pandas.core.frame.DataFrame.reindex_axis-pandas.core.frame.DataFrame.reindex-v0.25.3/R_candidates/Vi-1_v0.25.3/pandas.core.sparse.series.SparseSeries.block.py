    @property
    def block(self):
        warnings.warn("SparseSeries.block is deprecated.", FutureWarning, stacklevel=2)
        return self._data._block
