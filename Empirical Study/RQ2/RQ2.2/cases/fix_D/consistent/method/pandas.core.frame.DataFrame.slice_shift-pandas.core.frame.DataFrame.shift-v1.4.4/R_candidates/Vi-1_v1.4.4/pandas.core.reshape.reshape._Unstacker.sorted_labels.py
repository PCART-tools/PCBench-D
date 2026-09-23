    @cache_readonly
    def sorted_labels(self):
        indexer, to_sort = self._indexer_and_to_sort
        return [line.take(indexer) for line in to_sort]
