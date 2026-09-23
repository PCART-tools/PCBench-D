def _assert_series_inner(
    left: Series,
    right: Series,
    *,
    check_dtype: bool,
    check_exact: bool,
    atol: float,
    rtol: float,
    nans_compare_equal: bool,
    categorical_as_str: bool,
) -> None:
    """Compare Series dtype + values."""
    if check_dtype and left.dtype != right.dtype:
        raise_assert_detail("Series", "Dtype mismatch", left.dtype, right.dtype)

    if left.null_count() != right.null_count():
        raise_assert_detail(
            "Series", "null_count is not equal", left.null_count(), right.null_count()
        )

    if categorical_as_str and left.dtype == Categorical:
        left = left.cast(Utf8)
        right = right.cast(Utf8)

    # create mask of which (if any) values are unequal
    unequal = left.ne_missing(right)

    # handle NaN values (which compare unequal to themselves)
    comparing_float_dtypes = left.dtype in FLOAT_DTYPES and right.dtype in FLOAT_DTYPES
    if unequal.any() and nans_compare_equal:
        # when both dtypes are scalar floats
        if comparing_float_dtypes:
            unequal = unequal & ~(
                (left.is_nan() & right.is_nan()).fill_null(F.lit(False))
            )

    # check nested dtypes in separate function
    if left.dtype.is_nested or right.dtype.is_nested:
        if _assert_series_nested(
            left=left.filter(unequal),
            right=right.filter(unequal),
            check_dtype=check_dtype,
            check_exact=check_exact,
            atol=atol,
            rtol=rtol,
            nans_compare_equal=nans_compare_equal,
            categorical_as_str=categorical_as_str,
        ):
            return

    try:
        can_be_subtracted = hasattr(dtype_to_py_type(left.dtype), "__sub__")
    except NotImplementedError:
        can_be_subtracted = False

    check_exact = (
        check_exact or not can_be_subtracted or left.is_boolean() or left.is_temporal()
    )

    # assert exact, or with tolerance
    if unequal.any():
        if check_exact:
            raise_assert_detail(
                "Series",
                "Exact value mismatch",
                left=list(left),
                right=list(right),
            )
        else:
            # apply check with tolerance (to the known-unequal matches).
            left, right = left.filter(unequal), right.filter(unequal)

            if all(tp in UNSIGNED_INTEGER_DTYPES for tp in (left.dtype, right.dtype)):
                # avoid potential "subtract-with-overflow" panic on uint math
                s_diff = Series(
                    "diff", [abs(v1 - v2) for v1, v2 in zip(left, right)], dtype=UInt64
                )
            else:
                s_diff = (left - right).abs()

            mismatch, nan_info = False, ""
            if ((s_diff > (atol + rtol * right.abs())).sum() != 0) or (
                left.is_null() != right.is_null()
            ).any():
                mismatch = True
            elif comparing_float_dtypes:
                # note: take special care with NaN values.
                # if NaNs don't compare as equal, any NaN in the left Series is
                # sufficient for a mismatch because the if condition above already
                # compares the null values.
                if not nans_compare_equal and left.is_nan().any():
                    nan_info = " (nans_compare_equal=False)"
                    mismatch = True
                elif (left.is_nan() != right.is_nan()).any():
                    nan_info = f" (nans_compare_equal={nans_compare_equal})"
                    mismatch = True

            if mismatch:
                raise_assert_detail(
                    "Series",
                    f"Value mismatch{nan_info}",
                    left=list(left),
                    right=list(right),
                )
