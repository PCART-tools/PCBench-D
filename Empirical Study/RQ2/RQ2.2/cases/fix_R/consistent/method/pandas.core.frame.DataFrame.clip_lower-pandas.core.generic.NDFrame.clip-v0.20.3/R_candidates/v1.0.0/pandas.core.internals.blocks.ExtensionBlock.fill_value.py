    @property
    def fill_value(self):
        # Used in reindex_indexer
        return self.values.dtype.na_value
