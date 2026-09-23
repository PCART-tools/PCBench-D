    def _groupby_op(
        self,
        *,
        how: str,
        has_dropped_na: bool,
        min_count: int,
        ngroups: int,
        ids: npt.NDArray[np.intp],
        **kwargs,
    ):
        dtype = self.dtype
        if dtype.kind == "M":
            # Adding/multiplying datetimes is not valid
            if how in ["sum", "prod", "cumsum", "cumprod", "var", "skew"]:
                raise TypeError(f"datetime64 type does not support {how} operations")
            if how in ["any", "all"]:
                # GH#34479
                warnings.warn(
                    f"'{how}' with datetime64 dtypes is deprecated and will raise in a "
                    f"future version. Use (obj != pd.Timestamp(0)).{how}() instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )

        elif isinstance(dtype, PeriodDtype):
            # Adding/multiplying Periods is not valid
            if how in ["sum", "prod", "cumsum", "cumprod", "var", "skew"]:
                raise TypeError(f"Period type does not support {how} operations")
            if how in ["any", "all"]:
                # GH#34479
                warnings.warn(
                    f"'{how}' with PeriodDtype is deprecated and will raise in a "
                    f"future version. Use (obj != pd.Period(0, freq)).{how}() instead.",
                    FutureWarning,
                    stacklevel=find_stack_level(),
                )
        else:
            # timedeltas we can add but not multiply
            if how in ["prod", "cumprod", "skew", "var"]:
                raise TypeError(f"timedelta64 type does not support {how} operations")

        # All of the functions implemented here are ordinal, so we can
        #  operate on the tz-naive equivalents
        npvalues = self._ndarray.view("M8[ns]")

        from pandas.core.groupby.ops import WrappedCythonOp

        kind = WrappedCythonOp.get_kind_from_how(how)
        op = WrappedCythonOp(how=how, kind=kind, has_dropped_na=has_dropped_na)

        res_values = op._cython_op_ndim_compat(
            npvalues,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=ids,
            mask=None,
            **kwargs,
        )

        if op.how in op.cast_blocklist:
            # i.e. how in ["rank"], since other cast_blocklist methods don't go
            #  through cython_operation
            return res_values

        # We did a view to M8[ns] above, now we go the other direction
        assert res_values.dtype == "M8[ns]"
        if how in ["std", "sem"]:
            from pandas.core.arrays import TimedeltaArray

            if isinstance(self.dtype, PeriodDtype):
                raise TypeError("'std' and 'sem' are not valid for PeriodDtype")
            self = cast("DatetimeArray | TimedeltaArray", self)
            new_dtype = f"m8[{self.unit}]"
            res_values = res_values.view(new_dtype)
            return TimedeltaArray(res_values)

        res_values = res_values.view(self._ndarray.dtype)
        return self._from_backing_data(res_values)
