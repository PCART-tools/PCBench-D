    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(
        self, target: AnyArrayLike
    ) -> Tuple[np.ndarray, np.ndarray]:
        target_as_index = ensure_index(target)

        # check that target_as_index IntervalIndex is compatible
        if isinstance(target_as_index, IntervalIndex):

            if self._is_non_comparable_own_type(target_as_index):
                # different closed or incompatible subtype -> no matches
                return (
                    np.repeat(-1, len(target_as_index)),
                    np.arange(len(target_as_index)),
                )

        if is_object_dtype(target_as_index) or isinstance(
            target_as_index, IntervalIndex
        ):
            # target_as_index might contain intervals: defer elementwise to get_loc
            return self._get_indexer_pointwise(target_as_index)

        else:
            target_as_index = self._maybe_convert_i8(target_as_index)
            indexer, missing = self._engine.get_indexer_non_unique(
                target_as_index.values
            )

        return ensure_platform_int(indexer), ensure_platform_int(missing)
