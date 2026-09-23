def _guard_sizes_oblivious(
    lhs_sizes: Sequence[Union[torch.SymInt, bool]],
    rhs_sizes: Sequence[Union[torch.SymInt, bool]],
) -> bool:
    """
    Leverage guard_size_oblivious to compare if two lists of int/symint are equal.
    Useful to compare sizes, strides etc.
    """

    return len(lhs_sizes) == len(rhs_sizes) and all(
        guard_size_oblivious(lhs_item == rhs_item)
        for lhs_item, rhs_item in zip(lhs_sizes, rhs_sizes)
    )
