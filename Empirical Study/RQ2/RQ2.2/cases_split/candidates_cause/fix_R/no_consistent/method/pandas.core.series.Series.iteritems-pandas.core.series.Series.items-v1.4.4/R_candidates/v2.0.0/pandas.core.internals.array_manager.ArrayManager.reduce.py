    def reduce(self: T, func: Callable) -> T:
        """
        Apply reduction function column-wise, returning a single-row ArrayManager.

        Parameters
        ----------
        func : reduction function

        Returns
        -------
        ArrayManager
        """
        result_arrays: list[np.ndarray] = []
        for i, arr in enumerate(self.arrays):
            res = func(arr, axis=0)

            # TODO NaT doesn't preserve dtype, so we need to ensure to create
            # a timedelta result array if original was timedelta
            # what if datetime results in timedelta? (eg std)
            dtype = arr.dtype if res is NaT else None
            result_arrays.append(
                sanitize_array([res], None, dtype=dtype)  # type: ignore[arg-type]
            )

        index = Index._simple_new(np.array([None], dtype=object))  # placeholder
        columns = self.items

        # error: Argument 1 to "ArrayManager" has incompatible type "List[ndarray]";
        # expected "List[Union[ndarray, ExtensionArray]]"
        new_mgr = type(self)(result_arrays, [index, columns])  # type: ignore[arg-type]
        return new_mgr
