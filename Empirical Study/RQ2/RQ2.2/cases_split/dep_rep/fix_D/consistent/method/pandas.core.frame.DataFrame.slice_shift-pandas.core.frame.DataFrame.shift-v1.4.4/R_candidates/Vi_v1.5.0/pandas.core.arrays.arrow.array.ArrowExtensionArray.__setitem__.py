    def __setitem__(self, key: int | slice | np.ndarray, value: Any) -> None:
        """Set one or more values inplace.

        Parameters
        ----------
        key : int, ndarray, or slice
            When called from, e.g. ``Series.__setitem__``, ``key`` will be
            one of

            * scalar int
            * ndarray of integers.
            * boolean ndarray
            * slice object

        value : ExtensionDtype.type, Sequence[ExtensionDtype.type], or object
            value or values to be set of ``key``.

        Returns
        -------
        None
        """
        key = check_array_indexer(self, key)
        indices = self._indexing_key_to_indices(key)
        value = self._maybe_convert_setitem_value(value)

        argsort = np.argsort(indices)
        indices = indices[argsort]

        if is_scalar(value):
            value = np.broadcast_to(value, len(self))
        elif len(indices) != len(value):
            raise ValueError("Length of indexer and values mismatch")
        else:
            value = np.asarray(value)[argsort]

        self._data = self._set_via_chunk_iteration(indices=indices, value=value)
