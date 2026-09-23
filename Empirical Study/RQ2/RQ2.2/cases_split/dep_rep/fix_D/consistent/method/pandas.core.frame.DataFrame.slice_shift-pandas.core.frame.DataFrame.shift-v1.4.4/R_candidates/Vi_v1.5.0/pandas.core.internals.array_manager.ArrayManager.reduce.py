    def reduce(
        self: T, func: Callable, ignore_failures: bool = False
    ) -> tuple[T, np.ndarray]:
        """
        Apply reduction function column-wise, returning a single-row ArrayManager.

        Parameters
        ----------
        func : reduction function
        ignore_failures : bool, default False
            Whether to drop columns where func raises TypeError.

        Returns
        -------
        ArrayManager
        np.ndarray
            Indexer of column indices that are retained.
        """
        result_arrays: list[np.ndarray] = []
        result_indices: list[int] = []
        for i, arr in enumerate(self.arrays):
            try:
                res = func(arr, axis=0)
            except TypeError:
                if not ignore_failures:
                    raise
            else:
                # TODO NaT doesn't preserve dtype, so we need to ensure to create
                # a timedelta result array if original was timedelta
                # what if datetime results in timedelta? (eg std)
                if res is NaT and is_timedelta64_ns_dtype(arr.dtype):
                    result_arrays.append(np.array(["NaT"], dtype="timedelta64[ns]"))
                else:
                    # error: Argument 1 to "append" of "list" has incompatible type
                    # "ExtensionArray"; expected "ndarray"
                    result_arrays.append(
                        sanitize_array([res], None)  # type: ignore[arg-type]
                    )
                result_indices.append(i)

        index = Index._simple_new(np.array([None], dtype=object))  # placeholder
        if ignore_failures:
            indexer = np.array(result_indices)
            columns = self.items[result_indices]
        else:
            indexer = np.arange(self.shape[0])
            columns = self.items

        # error: Argument 1 to "ArrayManager" has incompatible type "List[ndarray]";
        # expected "List[Union[ndarray, ExtensionArray]]"
        new_mgr = type(self)(result_arrays, [index, columns])  # type: ignore[arg-type]
        return new_mgr, indexer
