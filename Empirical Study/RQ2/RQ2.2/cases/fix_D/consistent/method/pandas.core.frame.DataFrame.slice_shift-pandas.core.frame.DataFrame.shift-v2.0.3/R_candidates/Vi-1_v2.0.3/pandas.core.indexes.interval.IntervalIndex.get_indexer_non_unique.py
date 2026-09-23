    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(
        self, target: Index
    ) -> tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        target = ensure_index(target)

        if not self._should_compare(target) and not self._should_partial_index(target):
            # e.g. IntervalIndex with different closed or incompatible subtype
            #  -> no matches
            return self._get_indexer_non_comparable(target, None, unique=False)

        elif isinstance(target, IntervalIndex):
            if self.left.is_unique and self.right.is_unique:
                # fastpath available even if we don't have self._index_as_unique
                indexer = self._get_indexer_unique_sides(target)
                missing = (indexer == -1).nonzero()[0]
            else:
                return self._get_indexer_pointwise(target)

        elif is_object_dtype(target.dtype) or not self._should_partial_index(target):
            # target might contain intervals: defer elementwise to get_loc
            return self._get_indexer_pointwise(target)

        else:
            # Note: this case behaves differently from other Index subclasses
            #  because IntervalIndex does partial-int indexing
            target = self._maybe_convert_i8(target)
            indexer, missing = self._engine.get_indexer_non_unique(target.values)

        return ensure_platform_int(indexer), ensure_platform_int(missing)
