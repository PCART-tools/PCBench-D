    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target):
        target = ensure_index(target)

        if target.is_boolean() and self.is_numeric():
            # Treat boolean labels passed to a numeric index as not found. Without
            # this fix False and True would be treated as 0 and 1 respectively.
            # (GH #16877)
            return self._get_indexer_non_comparable(target, method=None, unique=False)

        pself, ptarget = self._maybe_promote(target)
        if pself is not self or ptarget is not target:
            return pself.get_indexer_non_unique(ptarget)

        if not self._should_compare(target):
            return self._get_indexer_non_comparable(target, method=None, unique=False)

        if not is_dtype_equal(self.dtype, target.dtype):
            # TODO: if object, could use infer_dtype to pre-empt costly
            #  conversion if still non-comparable?
            dtype = find_common_type([self.dtype, target.dtype])
            if (
                dtype.kind in ["i", "u"]
                and is_categorical_dtype(target.dtype)
                and target.hasnans
            ):
                # FIXME: find_common_type incorrect with Categorical GH#38240
                # FIXME: some cases where float64 cast can be lossy?
                dtype = np.dtype(np.float64)

            this = self.astype(dtype, copy=False)
            that = target.astype(dtype, copy=False)
            return this.get_indexer_non_unique(that)

        if is_categorical_dtype(target.dtype):
            tgt_values = np.asarray(target)
        else:
            tgt_values = target._get_engine_target()

        indexer, missing = self._engine.get_indexer_non_unique(tgt_values)
        return ensure_platform_int(indexer), missing
