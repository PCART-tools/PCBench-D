    def _getitem_nocopy(self, key: list):
        """
        Behaves like __getitem__, but returns a view in cases where __getitem__
        would make a copy.
        """
        # TODO(CoW): can be removed if/when we are always Copy-on-Write
        indexer = self.columns._get_indexer_strict(key, "columns")[1]
        new_axis = self.columns[indexer]

        new_mgr = self._mgr.reindex_indexer(
            new_axis,
            indexer,
            axis=0,
            allow_dups=True,
            copy=False,
            only_slice=True,
        )
        return self._constructor_from_mgr(new_mgr, axes=new_mgr.axes)
