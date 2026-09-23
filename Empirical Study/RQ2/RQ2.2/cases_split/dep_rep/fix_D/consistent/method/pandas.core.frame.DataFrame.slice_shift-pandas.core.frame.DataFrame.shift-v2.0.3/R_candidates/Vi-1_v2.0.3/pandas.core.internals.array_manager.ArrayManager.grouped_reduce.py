    def grouped_reduce(self: T, func: Callable) -> T:
        """
        Apply grouped reduction function columnwise, returning a new ArrayManager.

        Parameters
        ----------
        func : grouped reduction function

        Returns
        -------
        ArrayManager
        """
        result_arrays: list[np.ndarray] = []
        result_indices: list[int] = []

        for i, arr in enumerate(self.arrays):
            # grouped_reduce functions all expect 2D arrays
            arr = ensure_block_shape(arr, ndim=2)
            res = func(arr)
            if res.ndim == 2:
                # reverse of ensure_block_shape
                assert res.shape[0] == 1
                res = res[0]

            result_arrays.append(res)
            result_indices.append(i)

        if len(result_arrays) == 0:
            nrows = 0
        else:
            nrows = result_arrays[0].shape[0]
        index = Index(range(nrows))

        columns = self.items

        # error: Argument 1 to "ArrayManager" has incompatible type "List[ndarray]";
        # expected "List[Union[ndarray, ExtensionArray]]"
        return type(self)(result_arrays, [index, columns])  # type: ignore[arg-type]
