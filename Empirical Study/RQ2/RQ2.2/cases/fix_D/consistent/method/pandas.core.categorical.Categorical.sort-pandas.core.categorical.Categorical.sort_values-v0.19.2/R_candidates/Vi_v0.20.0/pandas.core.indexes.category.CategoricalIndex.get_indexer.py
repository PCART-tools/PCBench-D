    @Appender(_index_shared_docs['get_indexer'] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        method = missing.clean_reindex_fill_method(method)
        target = ibase._ensure_index(target)

        if self.equals(target):
            return np.arange(len(self), dtype='intp')

        if method == 'pad' or method == 'backfill':
            raise NotImplementedError("method='pad' and method='backfill' not "
                                      "implemented yet for CategoricalIndex")
        elif method == 'nearest':
            raise NotImplementedError("method='nearest' not implemented yet "
                                      'for CategoricalIndex')

        if (isinstance(target, CategoricalIndex) and
                self.values.is_dtype_equal(target)):
            # we have the same codes
            codes = target.codes
        else:
            if isinstance(target, CategoricalIndex):
                code_indexer = self.categories.get_indexer(target.categories)
                codes = take_1d(code_indexer, target.codes, fill_value=-1)
            else:
                codes = self.categories.get_indexer(target)

        indexer, _ = self._engine.get_indexer_non_unique(codes)

        return _ensure_platform_int(indexer)
