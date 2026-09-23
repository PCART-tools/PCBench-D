    def _apply_blockwise(
        self,
        homogeneous_func: Callable[..., ArrayLike],
        name: str,
        numeric_only: bool = False,
    ) -> DataFrame | Series:
        """
        Apply the given function to the DataFrame broken down into homogeneous
        sub-frames.
        """
        self._validate_numeric_only(name, numeric_only)
        if self._selected_obj.ndim == 1:
            return self._apply_series(homogeneous_func, name)

        obj = self._create_data(self._selected_obj, numeric_only)
        if name == "count":
            # GH 12541: Special case for count where we support date-like types
            obj = notna(obj).astype(int)
            obj._mgr = obj._mgr.consolidate()

        if self.axis == 1:
            obj = obj.T

        taker = []
        res_values = []
        for i, arr in enumerate(obj._iter_column_arrays()):
            # GH#42736 operate column-wise instead of block-wise
            # As of 2.0, hfunc will raise for nuisance columns
            try:
                arr = self._prep_values(arr)
            except (TypeError, NotImplementedError) as err:
                raise DataError(
                    f"Cannot aggregate non-numeric type: {arr.dtype}"
                ) from err
            res = homogeneous_func(arr)
            res_values.append(res)
            taker.append(i)

        index = self._slice_axis_for_step(
            obj.index, res_values[0] if len(res_values) > 0 else None
        )
        df = type(obj)._from_arrays(
            res_values,
            index=index,
            columns=obj.columns.take(taker),
            verify_integrity=False,
        )

        if self.axis == 1:
            df = df.T

        return self._resolve_output(df, obj)
