    def _convert_slice_indexer(self, key, typ=None):
        """ convert a slice indexer. disallow floats in the start/stop/step """

        if typ == 'iloc':
            return self._convert_slice_indexer_iloc(key)

        return super(MultiIndex, self)._convert_slice_indexer(key, typ=typ)
