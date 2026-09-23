    def _slice(self, slobj, axis=0, typ=None):
        slobj = self.index._convert_slice_indexer(slobj, typ=typ or 'getitem')
        return self._get_values(slobj)
