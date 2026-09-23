    def _slice(self, slobj, axis=0, raise_on_error=False, typ=None):
        if raise_on_error:
            _check_slice_bounds(slobj, self.values)
        slobj = self.index._convert_slice_indexer(slobj, typ=typ or 'getitem')
        return self._constructor(self.values[slobj],
                                 index=self.index[slobj]).__finalize__(self)
