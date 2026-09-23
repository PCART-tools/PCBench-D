    def _reindex_indexer_items(self, new_items, indexer, fill_value):
        # equiv to a reindex
        return self.reindex(new_items, indexer=indexer, fill_value=fill_value,
                            copy=False)
