    def reindex_axis0_with_method(self, new_axis, indexer=None, method=None,
                                  fill_value=None, limit=None, copy=True):
        if method is None:
            indexer = None
        return self.reindex(new_axis, indexer=indexer, method=method,
                            fill_value=fill_value, limit=limit, copy=copy)
