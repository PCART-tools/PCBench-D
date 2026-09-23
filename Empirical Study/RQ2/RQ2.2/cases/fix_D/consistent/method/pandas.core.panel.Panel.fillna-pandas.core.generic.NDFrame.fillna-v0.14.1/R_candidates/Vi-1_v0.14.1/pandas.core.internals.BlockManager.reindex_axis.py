    def reindex_axis(self, new_index, axis, method=None, limit=None,
                     fill_value=None, copy=True):
        """
        Conform block manager to new index.
        """
        new_index = _ensure_index(new_index)
        new_index, indexer = self.axes[axis].reindex(
            new_index, method=method, limit=limit, copy_if_needed=True)

        return self.reindex_indexer(new_index, indexer, axis=axis,
                                    fill_value=fill_value, copy=copy)
