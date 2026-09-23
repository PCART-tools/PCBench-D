    @Appender(_index_shared_docs["get_indexer"] % _index_doc_kwargs)
    @final
    def get_indexer(
        self,
        target,
        method: ReindexMethod | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> npt.NDArray[np.intp]:
        method = clean_reindex_fill_method(method)
        orig_target = target
        target = self._maybe_cast_listlike_indexer(target)

        self._check_indexing_method(method, limit, tolerance)

        if not self._index_as_unique:
            raise InvalidIndexError(self._requires_unique_msg)

        if len(target) == 0:
            return np.array([], dtype=np.intp)

        if not self._should_compare(target) and not self._should_partial_index(target):
            # IntervalIndex get special treatment bc numeric scalars can be
            #  matched to Interval scalars
            return self._get_indexer_non_comparable(target, method=method, unique=True)

        if isinstance(self.dtype, CategoricalDtype):
            # _maybe_cast_listlike_indexer ensures target has our dtype
            #  (could improve perf by doing _should_compare check earlier?)
            assert self.dtype == target.dtype

            indexer = self._engine.get_indexer(target.codes)
            if self.hasnans and target.hasnans:
                # After _maybe_cast_listlike_indexer, target elements which do not
                # belong to some category are changed to NaNs
                # Mask to track actual NaN values compared to inserted NaN values
                # GH#45361
                target_nans = isna(orig_target)
                loc = self.get_loc(np.nan)
                mask = target.isna()
                indexer[target_nans] = loc
                indexer[mask & ~target_nans] = -1
            return indexer

        if isinstance(target.dtype, CategoricalDtype):
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

        if self.dtype == target.dtype and self.equals(target):
            # Only call equals if we have same dtype to avoid inference/casting
            return np.arange(len(target), dtype=np.intp)

        if self.dtype != target.dtype and not self._should_partial_index(target):
            # _should_partial_index e.g. IntervalIndex with numeric scalars
            #  that can be matched to Interval scalars.
            dtype = self._find_common_type_compat(target)

            this = self.astype(dtype, copy=False)
            target = target.astype(dtype, copy=False)
            return this._get_indexer(
                target, method=method, limit=limit, tolerance=tolerance
            )

        return self._get_indexer(target, method, limit, tolerance)
