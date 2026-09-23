    def _cython_operation(
        self, kind: str, values, how: str, axis, min_count: int = -1, **kwargs
    ) -> Tuple[np.ndarray, Optional[List[str]]]:
        """
        Returns the values of a cython operation as a Tuple of [data, names].

        Names is only useful when dealing with 2D results, like ohlc
        (see self._name_functions).
        """

        assert kind in ["transform", "aggregate"]
        orig_values = values

        if values.ndim > 2:
            raise NotImplementedError("number of dimensions is currently limited to 2")
        elif values.ndim == 2:
            # Note: it is *not* the case that axis is always 0 for 1-dim values,
            #  as we can have 1D ExtensionArrays that we need to treat as 2D
            assert axis == 1, axis

        # can we do this operation with our cython functions
        # if not raise NotImplementedError

        # we raise NotImplemented if this is an invalid operation
        # entirely, e.g. adding datetimes

        # categoricals are only 1d, so we
        # are not setup for dim transforming
        if is_categorical_dtype(values) or is_sparse(values):
            raise NotImplementedError(f"{values.dtype} dtype not supported")
        elif is_datetime64_any_dtype(values):
            if how in ["add", "prod", "cumsum", "cumprod"]:
                raise NotImplementedError(
                    f"datetime64 type does not support {how} operations"
                )
        elif is_timedelta64_dtype(values):
            if how in ["prod", "cumprod"]:
                raise NotImplementedError(
                    f"timedelta64 type does not support {how} operations"
                )

        if is_datetime64tz_dtype(values.dtype):
            # Cast to naive; we'll cast back at the end of the function
            # TODO: possible need to reshape?  kludge can be avoided when
            #  2D EA is allowed.
            values = values.view("M8[ns]")

        is_datetimelike = needs_i8_conversion(values.dtype)
        is_numeric = is_numeric_dtype(values.dtype)

        if is_datetimelike:
            values = values.view("int64")
            is_numeric = True
        elif is_bool_dtype(values.dtype):
            values = ensure_float64(values)
        elif is_integer_dtype(values):
            # we use iNaT for the missing value on ints
            # so pre-convert to guard this condition
            if (values == iNaT).any():
                values = ensure_float64(values)
            else:
                values = ensure_int_or_float(values)
        elif is_numeric and not is_complex_dtype(values):
            values = ensure_float64(values)
        else:
            values = values.astype(object)

        arity = self._cython_arity.get(how, 1)

        vdim = values.ndim
        swapped = False
        if vdim == 1:
            values = values[:, None]
            out_shape = (self.ngroups, arity)
        else:
            if axis > 0:
                swapped = True
                assert axis == 1, axis
                values = values.T
            if arity > 1:
                raise NotImplementedError(
                    "arity of more than 1 is not supported for the 'how' argument"
                )
            out_shape = (self.ngroups,) + values.shape[1:]

        func, values = self._get_cython_func_and_vals(kind, how, values, is_numeric)

        if how == "rank":
            out_dtype = "float"
        else:
            if is_numeric:
                out_dtype = f"{values.dtype.kind}{values.dtype.itemsize}"
            else:
                out_dtype = "object"

        codes, _, _ = self.group_info

        if kind == "aggregate":
            result = _maybe_fill(
                np.empty(out_shape, dtype=out_dtype), fill_value=np.nan
            )
            counts = np.zeros(self.ngroups, dtype=np.int64)
            result = self._aggregate(
                result, counts, values, codes, func, is_datetimelike, min_count
            )
        elif kind == "transform":
            result = _maybe_fill(
                np.empty_like(values, dtype=out_dtype), fill_value=np.nan
            )

            # TODO: min_count
            result = self._transform(
                result, values, codes, func, is_datetimelike, **kwargs
            )

        if is_integer_dtype(result) and not is_datetimelike:
            mask = result == iNaT
            if mask.any():
                result = result.astype("float64")
                result[mask] = np.nan
        elif (
            how == "add"
            and is_integer_dtype(orig_values.dtype)
            and is_extension_array_dtype(orig_values.dtype)
        ):
            # We need this to ensure that Series[Int64Dtype].resample().sum()
            # remains int64 dtype.
            # Two options for avoiding this special case
            # 1. mask-aware ops and avoid casting to float with NaN above
            # 2. specify the result dtype when calling this method
            result = result.astype("int64")

        if kind == "aggregate" and self._filter_empty_groups and not counts.all():
            assert result.ndim != 2
            result = result[counts > 0]

        if vdim == 1 and arity == 1:
            result = result[:, 0]

        names: Optional[List[str]] = self._name_functions.get(how, None)

        if swapped:
            result = result.swapaxes(0, axis)

        if is_datetime64tz_dtype(orig_values.dtype) or is_period_dtype(
            orig_values.dtype
        ):
            # We need to use the constructors directly for these dtypes
            # since numpy won't recognize them
            # https://github.com/pandas-dev/pandas/issues/31471
            result = type(orig_values)(result.astype(np.int64), dtype=orig_values.dtype)
        elif is_datetimelike and kind == "aggregate":
            result = result.astype(orig_values.dtype)

        return result, names
