def assert_series_equal(
    left: Series,
    right: Series,
    *,
    check_dtype: bool = True,
    check_names: bool = True,
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
        the series to compare.
    right
        the series to compare with.
    check_dtype
        if True, data types need to match exactly.
    check_names
        if True, names need to match.
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
    >>> from polars.testing import assert_series_equal
    >>> s1 = pl.Series([1, 2, 3])
    >>> s2 = pl.Series([2, 3, 4])
    >>> assert_series_equal(s1, s2)  # doctest: +SKIP

    """
    if not (
        isinstance(left, Series)  # type: ignore[redundant-expr]
        and isinstance(right, Series)
    ):
        raise_assert_detail("Inputs", "unexpected input types", type(left), type(right))

    if len(left) != len(right):
        raise_assert_detail("Series", "length mismatch", len(left), len(right))

    if check_names and left.name != right.name:
        raise_assert_detail("Series", "name mismatch", left.name, right.name)

    _assert_series_inner(
        left,
        right,
        check_dtype=check_dtype,
        check_exact=check_exact,
        atol=atol,
        rtol=rtol,
        nans_compare_equal=nans_compare_equal,
        categorical_as_str=categorical_as_str,
    )
