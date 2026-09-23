    @cache_readonly
    def is_monotonic_increasing(self) -> bool:
        """
        Return a boolean if the values are equal or increasing.
        """
        if any(-1 in code for code in self.codes):
            return False

        if all(level.is_monotonic_increasing for level in self.levels):
            # If each level is sorted, we can operate on the codes directly. GH27495
            return libalgos.is_lexsorted(
                [x.astype("int64", copy=False) for x in self.codes]
            )

        # reversed() because lexsort() wants the most significant key last.
        values = [
            self._get_level_values(i)._values for i in reversed(range(len(self.levels)))
        ]
        try:
            # error: Argument 1 to "lexsort" has incompatible type
            # "List[Union[ExtensionArray, ndarray[Any, Any]]]";
            # expected "Union[_SupportsArray[dtype[Any]],
            # _NestedSequence[_SupportsArray[dtype[Any]]], bool,
            # int, float, complex, str, bytes, _NestedSequence[Union
            # [bool, int, float, complex, str, bytes]]]"
            sort_order = np.lexsort(values)  # type: ignore[arg-type]
            return Index(sort_order).is_monotonic_increasing
        except TypeError:

            # we have mixed types and np.lexsort is not happy
            return Index(self._values).is_monotonic_increasing
