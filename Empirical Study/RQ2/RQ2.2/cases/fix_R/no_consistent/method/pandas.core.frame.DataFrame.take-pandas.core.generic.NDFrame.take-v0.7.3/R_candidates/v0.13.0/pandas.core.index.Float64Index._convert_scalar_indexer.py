    def _convert_scalar_indexer(self, key, typ=None):

        if typ == 'iloc':
            return super(Float64Index, self)._convert_scalar_indexer(key,
                                                                     typ=typ)
        return key
