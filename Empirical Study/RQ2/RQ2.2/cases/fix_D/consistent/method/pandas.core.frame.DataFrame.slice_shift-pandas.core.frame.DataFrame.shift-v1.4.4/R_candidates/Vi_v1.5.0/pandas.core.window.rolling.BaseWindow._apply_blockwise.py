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

        def hfunc(values: ArrayLike) -> ArrayLike:
            values = self._prep_values(values)
            return homogeneous_func(values)

        if self.axis == 1:
            obj = obj.T

        taker = []
        res_values = []
        for i, arr in enumerate(obj._iter_column_arrays()):
            # GH#42736 operate column-wise instead of block-wise
            try:
                res = hfunc(arr)
            except (TypeError, NotImplementedError):
                pass
            else:
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

        if 0 != len(res_values) != len(obj.columns):
            # GH#42738 ignore_failures dropped nuisance columns
            dropped = obj.columns.difference(obj.columns.take(taker))
            warnings.warn(
                "Dropping of nuisance columns in rolling operations "
                "is deprecated; in a future version this will raise TypeError. "
                "Select only valid columns before calling the operation. "
                f"Dropped columns were {dropped}",
                FutureWarning,
                stacklevel=find_stack_level(inspect.currentframe()),
            )

        return self._resolve_output(df, obj)
