    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    @final
    def get_indexer(
        self,
        target,
        method: str_t | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> np.ndarray:
        # returned ndarray is np.intp
        method = missing.clean_reindex_fill_method(method)
        target = self._maybe_cast_listlike_indexer(target)

        self._check_indexing_method(method, limit, tolerance)

        if not self._index_as_unique:
            raise InvalidIndexError(self._requires_unique_msg)

        if not self._should_compare(target) and not is_interval_dtype(self.dtype):
            # IntervalIndex get special treatment bc numeric scalars can be
            #  matched to Interval scalars
            return self._get_indexer_non_comparable(target, method=method, unique=True)

        if is_categorical_dtype(self.dtype):
            # _maybe_cast_listlike_indexer ensures target has our dtype
            #  (could improve perf by doing _should_compare check earlier?)
            assert is_dtype_equal(self.dtype, target.dtype)

            indexer = self._engine.get_indexer(target.codes)
            if self.hasnans and target.hasnans:
                loc = self.get_loc(np.nan)
                mask = target.isna()
                indexer[mask] = loc
            return indexer

        if is_categorical_dtype(target.dtype):
            # potential fastpath
            # get an indexer for unique categories then propagate to codes via take_nd
            # get_indexer instead of _get_indexer needed for MultiIndex cases
            #  e.g. test_append_different_columns_types
            categories_indexer = self.get_indexer(target.categories)

            indexer = algos.take_nd(categories_indexer, target.codes, fill_value=-1)

            if (not self._is_multi and self.hasnans) and target.hasnans:
                # Exclude MultiIndex because hasnans raises NotImplementedError
                # we should only get here if we are unique, so loc is an integer
                # GH#41934
                loc = self.get_loc(np.nan)
                mask = target.isna()
                indexer[mask] = loc

            return ensure_platform_int(indexer)

        pself, ptarget = self._maybe_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer(
                ptarget, method=method, limit=limit, tolerance=tolerance
            )

        return self._get_indexer(target, method, limit, tolerance)
