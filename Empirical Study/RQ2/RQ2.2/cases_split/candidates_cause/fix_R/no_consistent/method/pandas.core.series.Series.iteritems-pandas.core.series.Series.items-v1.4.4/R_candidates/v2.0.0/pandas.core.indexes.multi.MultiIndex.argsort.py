    def argsort(self, *args, **kwargs) -> npt.NDArray[np.intp]:
        if len(args) == 0 and len(kwargs) == 0:
            # lexsort is significantly faster than self._values.argsort()
            target = self._sort_levels_monotonic(raise_if_incomparable=True)
            return lexsort_indexer(target._get_codes_for_sorting())
        return self._values.argsort(*args, **kwargs)
