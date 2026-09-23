    def _get_indexer(
        self,
        target: Index,
        method: str | None = None,
        limit: int | None = None,
        tolerance: Any | None = None,
    ) -> np.ndarray:
        # returned ndarray is np.intp

        if isinstance(target, IntervalIndex):
            # equal indexes -> 1:1 positional match
            if self.equals(target):
                return np.arange(len(self), dtype="intp")

            if not self._should_compare(target):
                return self._get_indexer_non_comparable(target, method, unique=True)

            # non-overlapping -> at most one match per interval in target
            # want exact matches -> need both left/right to match, so defer to
            # left/right get_indexer, compare elementwise, equality -> match
            left_indexer = self.left.get_indexer(target.left)
            right_indexer = self.right.get_indexer(target.right)
            indexer = np.where(left_indexer == right_indexer, left_indexer, -1)

        elif not is_object_dtype(target):
            # homogeneous scalar index: use IntervalTree
            target = self._maybe_convert_i8(target)
            indexer = self._engine.get_indexer(target.values)
        else:
            # heterogeneous scalar index: defer elementwise to get_loc
            return self._get_indexer_pointwise(target)[0]

        return ensure_platform_int(indexer)
