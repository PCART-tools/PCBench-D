    @final
    def _call_cython_op(
        self,
        values: np.ndarray,  # np.ndarray[ndim=2]
        *,
        min_count: int,
        ngroups: int,
        comp_ids: np.ndarray,
        mask: np.ndarray | None,
        result_mask: np.ndarray | None,
        **kwargs,
    ) -> np.ndarray:  # np.ndarray[ndim=2]
        orig_values = values

        dtype = values.dtype
        is_numeric = is_numeric_dtype(dtype)

        is_datetimelike = needs_i8_conversion(dtype)

        if is_datetimelike:
            values = values.view("int64")
            is_numeric = True
        elif is_bool_dtype(dtype):
            values = values.astype("int64")
        elif is_integer_dtype(dtype):
            # GH#43329 If the dtype is explicitly of type uint64 the type is not
            # changed to prevent overflow.
            if dtype != np.uint64:
                values = values.astype(np.int64, copy=False)
        elif is_numeric:
            if not is_complex_dtype(dtype):
                values = ensure_float64(values)

        values = values.T
        if mask is not None:
            mask = mask.T
            if result_mask is not None:
                result_mask = result_mask.T

        out_shape = self._get_output_shape(ngroups, values)
        func, values = self.get_cython_func_and_vals(values, is_numeric)
        out_dtype = self.get_out_dtype(values.dtype)

        result = maybe_fill(np.empty(out_shape, dtype=out_dtype))
        if self.kind == "aggregate":
            counts = np.zeros(ngroups, dtype=np.int64)
            if self.how in ["min", "max", "mean"]:
                func(
                    result,
                    counts,
                    values,
                    comp_ids,
                    min_count,
                    mask=mask,
                    result_mask=result_mask,
                    is_datetimelike=is_datetimelike,
                )
            elif self.how in ["add"]:
                # We support datetimelike
                func(
                    result,
                    counts,
                    values,
                    comp_ids,
                    min_count,
                    datetimelike=is_datetimelike,
                )
            else:
                func(result, counts, values, comp_ids, min_count)
        else:
            # TODO: min_count
            if self.uses_mask():
                func(
                    result,
                    values,
                    comp_ids,
                    ngroups,
                    is_datetimelike,
                    mask=mask,
                    **kwargs,
                )
            else:
                func(result, values, comp_ids, ngroups, is_datetimelike, **kwargs)

        if self.kind == "aggregate":
            # i.e. counts is defined.  Locations where count<min_count
            # need to have the result set to np.nan, which may require casting,
            # see GH#40767
            if is_integer_dtype(result.dtype) and not is_datetimelike:
                cutoff = max(1, min_count)
                empty_groups = counts < cutoff
                if empty_groups.any():
                    # Note: this conversion could be lossy, see GH#40767
                    result = result.astype("float64")
                    result[empty_groups] = np.nan

        result = result.T

        if self.how not in self.cast_blocklist:
            # e.g. if we are int64 and need to restore to datetime64/timedelta64
            # "rank" is the only member of cast_blocklist we get here
            res_dtype = self._get_result_dtype(orig_values.dtype)
            op_result = maybe_downcast_to_dtype(result, res_dtype)
        else:
            op_result = result

        # error: Incompatible return value type (got "Union[ExtensionArray, ndarray]",
        # expected "ndarray")
        return op_result  # type: ignore[return-value]
