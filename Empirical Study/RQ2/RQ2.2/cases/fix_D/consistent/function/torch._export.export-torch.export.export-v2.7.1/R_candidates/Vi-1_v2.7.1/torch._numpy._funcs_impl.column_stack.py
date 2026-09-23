def column_stack(
    tup: Sequence[ArrayLike],
    *,
    dtype: Optional[DTypeLike] = None,
    casting: Optional[CastingModes] = "same_kind",
):
    # XXX: in numpy 1.24 column_stack does not have dtype and casting keywords
    # but row_stack does. (because row_stack is an alias for vstack, really).
    # Hence add these keywords here for consistency.
    _concat_check(tup, dtype, out=None)
    tensors = _concat_cast_helper(tup, dtype=dtype, casting=casting)
    return torch.column_stack(tensors)
