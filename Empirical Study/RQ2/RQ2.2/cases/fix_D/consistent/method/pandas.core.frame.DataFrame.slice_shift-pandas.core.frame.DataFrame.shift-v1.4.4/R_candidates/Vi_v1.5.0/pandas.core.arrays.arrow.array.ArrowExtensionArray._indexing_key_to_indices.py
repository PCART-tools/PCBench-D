    def _indexing_key_to_indices(
        self, key: int | slice | np.ndarray
    ) -> npt.NDArray[np.intp]:
        """
        Convert indexing key for self into positional indices.

        Parameters
        ----------
        key : int | slice | np.ndarray

        Returns
        -------
        npt.NDArray[np.intp]
        """
        n = len(self)
        if isinstance(key, slice):
            indices = np.arange(n)[key]
        elif is_integer(key):
            # error: Invalid index type "List[Union[int, ndarray[Any, Any]]]"
            # for "ndarray[Any, dtype[signedinteger[Any]]]"; expected type
            # "Union[SupportsIndex, _SupportsArray[dtype[Union[bool_,
            # integer[Any]]]], _NestedSequence[_SupportsArray[dtype[Union
            # [bool_, integer[Any]]]]], _NestedSequence[Union[bool, int]]
            # , Tuple[Union[SupportsIndex, _SupportsArray[dtype[Union[bool_
            # , integer[Any]]]], _NestedSequence[_SupportsArray[dtype[Union
            # [bool_, integer[Any]]]]], _NestedSequence[Union[bool, int]]], ...]]"
            indices = np.arange(n)[[key]]  # type: ignore[index]
        elif is_bool_dtype(key):
            key = np.asarray(key)
            if len(key) != n:
                raise ValueError("Length of indexer and values mismatch")
            indices = key.nonzero()[0]
        else:
            key = np.asarray(key)
            indices = np.arange(n)[key]
        return indices
