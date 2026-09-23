    def _apply_tablewise(
        self, homogeneous_func: Callable[..., ArrayLike], name: str | None = None
    ) -> DataFrame | Series:
        """
        Apply the given function to the DataFrame across the entire object
        """
        if self._selected_obj.ndim == 1:
            raise ValueError("method='table' not applicable for Series objects.")
        obj = self._create_data(self._selected_obj)
        values = self._prep_values(obj.to_numpy())
        values = values.T if self.axis == 1 else values
        result = homogeneous_func(values)
        result = result.T if self.axis == 1 else result
        out = obj._constructor(result, index=obj.index, columns=obj.columns)

        return self._resolve_output(out, obj)
