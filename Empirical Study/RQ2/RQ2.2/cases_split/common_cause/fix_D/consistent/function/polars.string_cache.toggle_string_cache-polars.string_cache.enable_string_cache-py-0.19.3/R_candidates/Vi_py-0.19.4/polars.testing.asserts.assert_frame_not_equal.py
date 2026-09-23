def assert_frame_not_equal(
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
    Raise AssertionError if `left` DOES equal `right`.

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
    >>> from polars.testing import assert_frame_not_equal
    >>> df1 = pl.DataFrame({"a": [1, 2, 3]})
    >>> df2 = pl.DataFrame({"a": [2, 3, 4]})
    >>> assert_frame_not_equal(df1, df2)

    """
    try:
        assert_frame_equal(
            left=left,
            right=right,
            check_column_order=check_column_order,
            check_row_order=check_row_order,
            check_dtype=check_dtype,
            check_exact=check_exact,
            rtol=rtol,
            atol=atol,
            nans_compare_equal=nans_compare_equal,
            categorical_as_str=categorical_as_str,
        )
    except AssertionError:
        return
    else:
        raise AssertionError("expected the input frames to be unequal")
