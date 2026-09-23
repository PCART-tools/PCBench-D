    def _wrap_min_count_reduction_result(
        self, name: str, result, *, skipna, min_count, axis
    ):
        if min_count == 0 and isinstance(result, np.ndarray):
            return self._maybe_mask_result(result, np.zeros(result.shape, dtype=bool))
        return self._wrap_reduction_result(name, result, skipna=skipna, axis=axis)
