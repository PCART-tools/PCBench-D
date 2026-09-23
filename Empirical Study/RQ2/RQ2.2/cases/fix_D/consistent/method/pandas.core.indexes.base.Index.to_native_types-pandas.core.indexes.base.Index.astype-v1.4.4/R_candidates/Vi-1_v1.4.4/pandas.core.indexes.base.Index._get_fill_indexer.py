    @final
    def _get_fill_indexer(
        self, target: Index, method: str_t, limit: int | None = None, tolerance=None
    ) -> npt.NDArray[np.intp]:

        if self._is_multi:
            # TODO: get_indexer_with_fill docstring says values must be _sorted_
            #  but that doesn't appear to be enforced
            # error: "IndexEngine" has no attribute "get_indexer_with_fill"
            return self._engine.get_indexer_with_fill(  # type: ignore[attr-defined]
                target=target._values, values=self._values, method=method, limit=limit
            )

        if self.is_monotonic_increasing and target.is_monotonic_increasing:
            target_values = target._get_engine_target()
            own_values = self._get_engine_target()

            if method == "pad":
                indexer = libalgos.pad(own_values, target_values, limit=limit)
            else:
                # i.e. "backfill"
                indexer = libalgos.backfill(own_values, target_values, limit=limit)
        else:
            indexer = self._get_fill_indexer_searchsorted(target, method, limit)
        if tolerance is not None and len(self):
            indexer = self._filter_indexer_tolerance(target, indexer, tolerance)
        return indexer
