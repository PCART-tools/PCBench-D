    @Appender(_index_shared_docs["get_indexer_non_unique"] % _index_doc_kwargs)
    def get_indexer_non_unique(
        self, target: AnyArrayLike
    ) -> Tuple[np.ndarray, np.ndarray]:
        target = ensure_index(target)

        # check that target IntervalIndex is compatible
        if isinstance(target, IntervalIndex):
            common_subtype = find_common_type(
                [self.dtype.subtype, target.dtype.subtype]
            )
            if self.closed != target.closed or is_object_dtype(common_subtype):
                # different closed or incompatible subtype -> no matches
                return np.repeat(-1, len(target)), np.arange(len(target))

        if is_object_dtype(target) or isinstance(target, IntervalIndex):
            # target might contain intervals: defer elementwise to get_loc
            indexer, missing = [], []
            for i, key in enumerate(target):
                try:
                    locs = self.get_loc(key)
                    if isinstance(locs, slice):
                        locs = np.arange(locs.start, locs.stop, locs.step, dtype="intp")
                    locs = np.array(locs, ndmin=1)
                except KeyError:
                    missing.append(i)
                    locs = np.array([-1])
                indexer.append(locs)
            indexer = np.concatenate(indexer)
        else:
            target = self._maybe_convert_i8(target)
            indexer, missing = self._engine.get_indexer_non_unique(target.values)

        return ensure_platform_int(indexer), ensure_platform_int(missing)
