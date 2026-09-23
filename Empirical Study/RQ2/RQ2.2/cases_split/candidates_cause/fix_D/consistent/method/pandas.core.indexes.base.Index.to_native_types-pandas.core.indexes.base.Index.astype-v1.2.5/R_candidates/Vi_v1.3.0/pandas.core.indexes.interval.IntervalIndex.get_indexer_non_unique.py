    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(self, target: Index) -> tuple[np.ndarray, np.ndarray]:
        # both returned ndarrays are np.intp
        target = ensure_index(target)

        if isinstance(target, IntervalIndex) and not self._should_compare(target):
            # different closed or incompatible subtype -> no matches
            return self._get_indexer_non_comparable(target, None, unique=False)

        elif is_object_dtype(target.dtype) or isinstance(target, IntervalIndex):
            # target might contain intervals: defer elementwise to get_loc
            return self._get_indexer_pointwise(target)

        else:
            # Note: this case behaves differently from other Index subclasses
            #  because IntervalIndex does partial-int indexing
            target = self._maybe_convert_i8(target)
            indexer, missing = self._engine.get_indexer_non_unique(target.values)

        return ensure_platform_int(indexer), ensure_platform_int(missing)
