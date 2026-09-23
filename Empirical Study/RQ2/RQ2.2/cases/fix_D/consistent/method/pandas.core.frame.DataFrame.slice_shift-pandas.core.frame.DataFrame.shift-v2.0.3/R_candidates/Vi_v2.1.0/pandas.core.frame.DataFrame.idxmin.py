    @doc(_shared_docs["idxmin"], numeric_only_default="False")
    def idxmin(
        self, axis: Axis = 0, skipna: bool = True, numeric_only: bool = False
    ) -> Series:
        axis = self._get_axis_number(axis)

        if self.empty and len(self.axes[axis]):
            axis_dtype = self.axes[axis].dtype
            return self._constructor_sliced(dtype=axis_dtype)

        if numeric_only:
            data = self._get_numeric_data()
        else:
            data = self

        res = data._reduce(
            nanops.nanargmin, "argmin", axis=axis, skipna=skipna, numeric_only=False
        )
        indices = res._values
        # indices will always be np.ndarray since axis is not N

        if (indices == -1).any():
            warnings.warn(
                f"The behavior of {type(self).__name__}.idxmin with all-NA "
                "values, or any-NA and skipna=False, is deprecated. In a future "
                "version this will raise ValueError",
                FutureWarning,
                stacklevel=find_stack_level(),
            )

        index = data._get_axis(axis)
        result = algorithms.take(
            index._values, indices, allow_fill=True, fill_value=index._na_value
        )
        final_result = data._constructor_sliced(result, index=data._get_agg_axis(axis))
        return final_result.__finalize__(self, method="idxmin")
