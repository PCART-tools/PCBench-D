    def _slice(self, slobj, axis=0, kind=None):
        slobj = self.index._convert_slice_indexer(slobj, kind=kind or "getitem")
        return self._get_values(slobj)
