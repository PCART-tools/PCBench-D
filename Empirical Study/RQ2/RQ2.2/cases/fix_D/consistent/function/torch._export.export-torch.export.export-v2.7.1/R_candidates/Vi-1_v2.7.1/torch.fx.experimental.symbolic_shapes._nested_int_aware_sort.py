def _nested_int_aware_sort(
    tup: tuple[Union[SymInt, int], int]
) -> tuple[int, Union[SymInt, int], int]:
    return (
        # Order nested ints by their coefficients.
        # 1 here to order nested ints after non-nested-ints.
        (1, tup[0].node.nested_int_coeff(), tup[1])
        if is_nested_int(tup[0])
        else (0, *tup)
    )
