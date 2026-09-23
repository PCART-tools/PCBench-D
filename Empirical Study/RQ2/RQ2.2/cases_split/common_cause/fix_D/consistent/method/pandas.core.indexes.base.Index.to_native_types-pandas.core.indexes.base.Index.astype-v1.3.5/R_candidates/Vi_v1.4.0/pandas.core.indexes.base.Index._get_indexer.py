    def _get_indexer(
        self,
        target: Index,
        method: str_t | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> npt.NDArray[np.intp]:
        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)

        if method in ["pad", "backfill"]:
            indexer = self._get_fill_indexer(target, method, limit, tolerance)
        elif method == "nearest":
            indexer = self._get_nearest_indexer(target, limit, tolerance)
        else:
            tgt_values = target._get_engine_target()
            if target._is_multi and self._is_multi:
                engine = self._engine
                # error: "IndexEngine" has no attribute "_extract_level_codes"
                tgt_values = engine._extract_level_codes(  # type: ignore[attr-defined]
                    target
                )

            indexer = self._engine.get_indexer(tgt_values)

        return ensure_platform_int(indexer)
