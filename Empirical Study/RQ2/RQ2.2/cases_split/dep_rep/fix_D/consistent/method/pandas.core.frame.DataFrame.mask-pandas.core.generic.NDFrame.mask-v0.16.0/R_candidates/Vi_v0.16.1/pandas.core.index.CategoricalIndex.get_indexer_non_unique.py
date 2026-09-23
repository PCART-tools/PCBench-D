    def get_indexer_non_unique(self, target):
        """ this is the same for a CategoricalIndex for get_indexer; the API returns the missing values as well """
        target = _ensure_index(target)

        if isinstance(target, CategoricalIndex):
            target = target.categories

        codes = self.categories.get_indexer(target)
        return self._engine.get_indexer_non_unique(codes)
