    @Appender(_index_shared_docs['get_indexer'] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        method = missing.clean_reindex_fill_method(method)
        target = ensure_index(target)

        # empty indexer
        if is_list_like(target) and not len(target):
            return ensure_platform_int(np.array([]))

        if not isinstance(target, MultiIndex):
            try:
                target = MultiIndex.from_tuples(target)
            except (TypeError, ValueError):

                # let's instead try with a straight Index
                if method is None:
                    return Index(self.values).get_indexer(target,
                                                          method=method,
                                                          limit=limit,
                                                          tolerance=tolerance)

        if not self.is_unique:
            raise ValueError('Reindexing only valid with uniquely valued '
                             'Index objects')

        if method == 'pad' or method == 'backfill':
            if tolerance is not None:
                raise NotImplementedError("tolerance not implemented yet "
                                          'for MultiIndex')
            indexer = self._engine.get_indexer(target, method, limit)
        elif method == 'nearest':
            raise NotImplementedError("method='nearest' not implemented yet "
                                      'for MultiIndex; see GitHub issue 9365')
        else:
            indexer = self._engine.get_indexer(target)

        return ensure_platform_int(indexer)
