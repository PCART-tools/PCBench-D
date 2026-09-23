    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target) -> tuple[np.ndarray, np.ndarray]:
        # both returned ndarrays are np.intp
        target = ensure_index(target)

        if not self._should_compare(target) and not is_interval_dtype(self.dtype):
            # IntervalIndex get special treatment bc numeric scalars can be
            #  matched to Interval scalars
            return self._get_indexer_non_comparable(target, method=None, unique=False)

        pself, ptarget = self._maybe_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer_non_unique(ptarget)

        if not is_dtype_equal(self.dtype, target.dtype):
            # TODO: if object, could use infer_dtype to preempt costly
            #  conversion if still non-comparable?
            dtype = self._find_common_type_compat(target)

            this = self.astype(dtype, copy=False)
            that = target.astype(dtype, copy=False)
            return this.get_indexer_non_unique(that)

        tgt_values = target._get_engine_target()

        indexer, missing = self._engine.get_indexer_non_unique(tgt_values)
        return ensure_platform_int(indexer), ensure_platform_int(missing)
