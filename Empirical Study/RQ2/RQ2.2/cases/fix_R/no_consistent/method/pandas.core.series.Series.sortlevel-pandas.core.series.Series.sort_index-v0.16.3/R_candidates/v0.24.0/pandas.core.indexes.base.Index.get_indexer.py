    @Appender(_index_shared_docs['get_indexer'] % _index_doc_kwargs)
    def get_indexer(self, target, method=None, limit=None, tolerance=None):
        method = missing.clean_reindex_fill_method(method)
        target = ensure_index(target)
        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)

        # Treat boolean labels passed to a numeric index as not found. Without
        # this fix False and True would be treated as 0 and 1 respectively.
        # (GH #16877)
        if target.is_boolean() and self.is_numeric():
            return ensure_platform_int(np.repeat(-1, target.size))

        pself, ptarget = self._maybe_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer(ptarget, method=method, limit=limit,
                                     tolerance=tolerance)

        if not is_dtype_equal(self.dtype, target.dtype):
            this = self.astype(object)
            target = target.astype(object)
            return this.get_indexer(target, method=method, limit=limit,
                                    tolerance=tolerance)

        if not self.is_unique:
            raise InvalidIndexError('Reindexing only valid with uniquely'
                                    ' valued Index objects')

        if method == 'pad' or method == 'backfill':
            indexer = self._get_fill_indexer(target, method, limit, tolerance)
        elif method == 'nearest':
            indexer = self._get_nearest_indexer(target, limit, tolerance)
        else:
            if tolerance is not None:
                raise ValueError('tolerance argument only valid if doing pad, '
                                 'backfill or nearest reindexing')
            if limit is not None:
                raise ValueError('limit argument only valid if doing pad, '
                                 'backfill or nearest reindexing')

            indexer = self._engine.get_indexer(target._ndarray_values)

        return ensure_platform_int(indexer)
