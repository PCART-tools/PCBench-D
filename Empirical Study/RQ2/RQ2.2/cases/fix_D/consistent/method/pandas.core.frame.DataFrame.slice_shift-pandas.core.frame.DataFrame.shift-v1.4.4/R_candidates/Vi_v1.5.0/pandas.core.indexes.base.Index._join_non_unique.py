    @final
    def _join_non_unique(
        self, other: Index, how: str_t = "left"
    ) -> tuple[Index, npt.NDArray[np.intp], npt.NDArray[np.intp]]:
        from pandas.core.reshape.merge import get_join_indexers

        # We only get here if dtypes match
        assert self.dtype == other.dtype

        left_idx, right_idx = get_join_indexers(
            [self._values], [other._values], how=how, sort=True
        )
        mask = left_idx == -1

        join_array = self._values.take(left_idx)
        right = other._values.take(right_idx)

        if isinstance(join_array, np.ndarray):
            # error: Argument 3 to "putmask" has incompatible type
            # "Union[ExtensionArray, ndarray[Any, Any]]"; expected
            # "Union[_SupportsArray[dtype[Any]], _NestedSequence[
            # _SupportsArray[dtype[Any]]], bool, int, float, complex,
            # str, bytes, _NestedSequence[Union[bool, int, float,
            # complex, str, bytes]]]"
            np.putmask(join_array, mask, right)  # type: ignore[arg-type]
        else:
            join_array._putmask(mask, right)

        join_index = self._wrap_joined_index(join_array, other)

        return join_index, left_idx, right_idx
