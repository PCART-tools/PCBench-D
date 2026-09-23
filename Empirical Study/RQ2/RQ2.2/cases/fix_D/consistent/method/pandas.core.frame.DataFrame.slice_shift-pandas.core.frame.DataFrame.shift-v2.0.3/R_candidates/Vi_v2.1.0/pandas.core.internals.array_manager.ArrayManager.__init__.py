    def __init__(
        self,
        arrays: list[np.ndarray | ExtensionArray],
        axes: list[Index],
        verify_integrity: bool = True,
    ) -> None:
        # Note: we are storing the axes in "_axes" in the (row, columns) order
        # which contrasts the order how it is stored in BlockManager
        self._axes = axes
        self.arrays = arrays

        if verify_integrity:
            self._axes = [ensure_index(ax) for ax in axes]
            arrays = [extract_pandas_array(x, None, 1)[0] for x in arrays]
            self.arrays = [maybe_coerce_values(arr) for arr in arrays]
            self._verify_integrity()
