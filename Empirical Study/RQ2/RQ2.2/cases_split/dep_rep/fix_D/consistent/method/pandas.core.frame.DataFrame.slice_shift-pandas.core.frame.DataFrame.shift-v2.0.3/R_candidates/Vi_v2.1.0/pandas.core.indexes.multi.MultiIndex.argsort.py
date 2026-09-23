    def argsort(
        self, *args, na_position: str = "last", **kwargs
    ) -> npt.NDArray[np.intp]:
        if len(args) == 0 and len(kwargs) == 0:
            # lexsort is significantly faster than self._values.argsort()
            target = self._sort_levels_monotonic(raise_if_incomparable=True)
            return lexsort_indexer(
                # error: Argument 1 to "lexsort_indexer" has incompatible type
                # "List[Categorical]"; expected "Union[List[Union[ExtensionArray,
                # ndarray[Any, Any]]], List[Series]]"
                target._get_codes_for_sorting(),  # type: ignore[arg-type]
                na_position=na_position,
            )
        return self._values.argsort(*args, **kwargs)
