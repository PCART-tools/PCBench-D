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
        from pandas.core.groupby.ops import WrappedCythonOp

        kind = WrappedCythonOp.get_kind_from_how(how)
        op = WrappedCythonOp(how=how, kind=kind, has_dropped_na=has_dropped_na)

        dtype = self.dtype
        if how in ["sum", "prod", "cumsum", "cumprod", "skew"]:
            raise TypeError(f"{dtype} type does not support {how} operations")
        if how in ["min", "max", "rank"] and not dtype.ordered:
            # raise TypeError instead of NotImplementedError to ensure we
            #  don't go down a group-by-group path, since in the empty-groups
            #  case that would fail to raise
            raise TypeError(f"Cannot perform {how} with non-ordered Categorical")
        if how not in ["rank", "any", "all", "first", "last", "min", "max"]:
            if kind == "transform":
                raise TypeError(f"{dtype} type does not support {how} operations")
            raise TypeError(f"{dtype} dtype does not support aggregation '{how}'")

        result_mask = None
        mask = self.isna()
        if how == "rank":
            assert self.ordered  # checked earlier
            npvalues = self._ndarray
        elif how in ["first", "last", "min", "max"]:
            npvalues = self._ndarray
            result_mask = np.zeros(ngroups, dtype=bool)
        else:
            # any/all
            npvalues = self.astype(bool)

        res_values = op._cython_op_ndim_compat(
            npvalues,
            min_count=min_count,
            ngroups=ngroups,
            comp_ids=ids,
            mask=mask,
            result_mask=result_mask,
            **kwargs,
        )

        if how in op.cast_blocklist:
            return res_values
        elif how in ["first", "last", "min", "max"]:
            res_values[result_mask == 1] = -1
        return self._from_backing_data(res_values)
