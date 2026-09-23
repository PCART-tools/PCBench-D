    def _get_indexer(
        self,
        target: Index,
        method: str_t | None = None,
        limit: int | None = None,
        tolerance=None,
    ) -> np.ndarray:
        if tolerance is not None:
            tolerance = self._convert_tolerance(tolerance, target)

        if not is_dtype_equal(self.dtype, target.dtype):
            dtype = self._find_common_type_compat(target)

            this = self.astype(dtype, copy=False)
            target = target.astype(dtype, copy=False)
            return this.get_indexer(
                target, method=method, limit=limit, tolerance=tolerance
            )

        if method in ["pad", "backfill"]:
            indexer = self._get_fill_indexer(target, method, limit, tolerance)
        elif method == "nearest":
            indexer = self._get_nearest_indexer(target, limit, tolerance)
        else:
            indexer = self._engine.get_indexer(target._get_engine_target())

        return ensure_platform_int(indexer)
