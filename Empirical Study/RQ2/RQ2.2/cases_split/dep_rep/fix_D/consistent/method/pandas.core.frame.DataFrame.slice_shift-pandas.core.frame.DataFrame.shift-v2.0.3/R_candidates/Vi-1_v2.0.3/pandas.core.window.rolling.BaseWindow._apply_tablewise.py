    def _apply_tablewise(
        self,
        homogeneous_func: Callable[..., ArrayLike],
        name: str | None = None,
        numeric_only: bool = False,
    ) -> DataFrame | Series:
        """
        Apply the given function to the DataFrame across the entire object
        """
        if self._selected_obj.ndim == 1:
            raise ValueError("method='table' not applicable for Series objects.")
        obj = self._create_data(self._selected_obj, numeric_only)
        values = self._prep_values(obj.to_numpy())
        values = values.T if self.axis == 1 else values
        result = homogeneous_func(values)
        result = result.T if self.axis == 1 else result
        index = self._slice_axis_for_step(obj.index, result)
        columns = (
            obj.columns
            if result.shape[1] == len(obj.columns)
            else obj.columns[:: self.step]
        )
        out = obj._constructor(result, index=index, columns=columns)

        return self._resolve_output(out, obj)
