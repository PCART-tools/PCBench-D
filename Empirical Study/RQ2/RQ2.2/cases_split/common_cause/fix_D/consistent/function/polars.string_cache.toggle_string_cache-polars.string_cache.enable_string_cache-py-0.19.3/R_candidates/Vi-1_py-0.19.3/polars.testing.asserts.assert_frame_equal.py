def assert_frame_equal(
    left: DataFrame | LazyFrame,
    right: DataFrame | LazyFrame,
    *,
    check_row_order: bool = True,
    check_column_order: bool = True,
    check_dtype: bool = True,
    check_exact: bool = False,
    rtol: float = 1.0e-5,
    atol: float = 1.0e-8,
    nans_compare_equal: bool = True,
    categorical_as_str: bool = False,
) -> None:
    """
    Raise detailed AssertionError if `left` does NOT equal `right`.

    Parameters
    ----------
    left
        the DataFrame to compare.
    right
        the DataFrame to compare with.
    check_row_order
        if False, frames will compare equal if the required rows are present,
        irrespective of the order in which they appear; as this requires
        sorting, you cannot set on frames that contain unsortable columns.
    check_column_order
        if False, frames will compare equal if the required columns are present,
        irrespective of the order in which they appear.
    check_dtype
        if True, data types need to match exactly.
    check_exact
        if False, test if values are within tolerance of each other
        (see `rtol` & `atol`).
    rtol
        relative tolerance for inexact checking. Fraction of values in `right`.
    atol
        absolute tolerance for inexact checking.
    nans_compare_equal
        if your assert/test requires float NaN != NaN, set this to False.
    categorical_as_str
        Cast categorical columns to string before comparing. Enabling this helps
        compare DataFrames that do not share the same string cache.

    Examples
    --------
    >>> from polars.testing import assert_frame_equal
    >>> df1 = pl.DataFrame({"a": [1, 2, 3]})
    >>> df2 = pl.DataFrame({"a": [2, 3, 4]})
    >>> assert_frame_equal(df1, df2)  # doctest: +SKIP
    AssertionError: Values for column 'a' are different.
    """
    if isinstance(left, LazyFrame) and isinstance(right, LazyFrame):
        left, right = left.collect(), right.collect()
        obj = "LazyFrames"
    elif isinstance(left, DataFrame) and isinstance(right, DataFrame):
        obj = "DataFrames"
    else:
        raise_assert_detail("Inputs", "Unexpected input types", type(left), type(right))

    if left.shape[0] != right.shape[0]:  # type: ignore[union-attr]
        raise_assert_detail(obj, "Length mismatch", left.shape, right.shape)  # type: ignore[union-attr]

    left_not_right = [c for c in left.columns if c not in right.columns]
    if left_not_right:
        raise AssertionError(
            f"columns {left_not_right!r} in left frame, but not in right"
        )
    right_not_left = [c for c in right.columns if c not in left.columns]
    if right_not_left:
        raise AssertionError(
            f"columns {right_not_left!r} in right frame, but not in left"
        )

    if check_column_order and left.columns != right.columns:
        raise AssertionError(
            f"columns are not in the same order:\n{left.columns!r}\n{right.columns!r}"
        )

    if not check_row_order:
        try:
            left = left.sort(by=left.columns)
            right = right.sort(by=left.columns)
        except ComputeError as exc:
            raise InvalidAssert(
                "cannot set 'check_row_order=False' on frame with unsortable columns"
            ) from exc

    # note: does not assume a particular column order
    for c in left.columns:
        try:
            _assert_series_inner(
                left[c],  # type: ignore[arg-type, index]
                right[c],  # type: ignore[arg-type, index]
                check_dtype=check_dtype,
                check_exact=check_exact,
                atol=atol,
                rtol=rtol,
                nans_compare_equal=nans_compare_equal,
                categorical_as_str=categorical_as_str,
            )
        except AssertionError as exc:
            msg = f"values for column {c!r} are different."
            raise AssertionError(msg) from exc
