    def _reindex_indexer(self, new_index, indexer, copy):
        if indexer is None:
            if copy:
                return self.copy()
            return self

        # be subclass-friendly
        new_values = algorithms.take_1d(self.get_values(), indexer)
        return self._constructor(new_values, index=new_index)
