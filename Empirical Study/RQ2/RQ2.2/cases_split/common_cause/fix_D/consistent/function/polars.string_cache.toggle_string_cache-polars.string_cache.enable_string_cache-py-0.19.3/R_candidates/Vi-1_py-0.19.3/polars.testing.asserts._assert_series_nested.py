def _assert_series_nested(
    left: Series,
    right: Series,
    *,
    check_dtype: bool,
    check_exact: bool,
    atol: float,
    rtol: float,
    nans_compare_equal: bool,
    categorical_as_str: bool,
) -> bool:
    # check that float values exist at _some_ level of nesting
    if not any(tp in FLOAT_DTYPES for tp in unpack_dtypes(left.dtype, right.dtype)):
        return False

    # compare nested lists element-wise
    elif left.dtype == List == right.dtype:
        for s1, s2 in zip(left, right):
            if s1 is None and s2 is None:
                if nans_compare_equal:
                    continue
                else:
                    raise_assert_detail(
                        "Series",
                        f"Nested value mismatch (nans_compare_equal={nans_compare_equal})",
                        s1,
                        s2,
                    )
            elif (s1 is None and s2 is not None) or (s2 is None and s1 is not None):
                raise_assert_detail("Series", "Nested value mismatch", s1, s2)
            elif len(s1) != len(s2):
                raise_assert_detail(
                    "Series", "Nested list length mismatch", len(s1), len(s2)
                )

            _assert_series_inner(
                s1,
                s2,
                check_dtype=check_dtype,
                check_exact=check_exact,
                atol=atol,
                rtol=rtol,
                nans_compare_equal=nans_compare_equal,
                categorical_as_str=categorical_as_str,
            )
        return True

    # unnest structs as series and compare
    elif left.dtype == Struct == right.dtype:
        ls, rs = left.struct.unnest(), right.struct.unnest()
        if len(ls.columns) != len(rs.columns):
            raise_assert_detail(
                "Series",
                "Nested struct fields mismatch",
                len(ls.columns),
                len(rs.columns),
            )
        elif len(ls) != len(rs):
            raise_assert_detail(
                "Series", "Nested struct length mismatch", len(ls), len(rs)
            )
        for s1, s2 in zip(ls, rs):
            _assert_series_inner(
                s1,
                s2,
                check_dtype=check_dtype,
                check_exact=check_exact,
                atol=atol,
                rtol=rtol,
                nans_compare_equal=nans_compare_equal,
                categorical_as_str=categorical_as_str,
            )
        return True
    else:
        # fall-back to outer codepath (if mismatched dtypes we would expect
        # the equality check to fail - unless ALL series values are null)
        return False
