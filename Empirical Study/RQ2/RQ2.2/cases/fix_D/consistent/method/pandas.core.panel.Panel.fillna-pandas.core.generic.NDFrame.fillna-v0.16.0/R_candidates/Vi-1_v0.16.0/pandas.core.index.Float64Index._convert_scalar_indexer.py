    def _convert_scalar_indexer(self, key, kind=None):
        if kind == 'iloc':
            return super(Float64Index, self)._convert_scalar_indexer(key,
                                                                     kind=kind)
        return key
