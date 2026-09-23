def concatenate_join_units(join_units, concat_axis, copy):
    """
    Concatenate values from several join units along selected axis.
    """
    if concat_axis == 0 and len(join_units) > 1:
        # Concatenating join units along ax0 is handled in _merge_blocks.
        raise AssertionError("Concatenating join units along axis0")

    empty_dtype, upcasted_na = get_empty_dtype_and_na(join_units)

    to_concat = [ju.get_reindexed_values(empty_dtype=empty_dtype,
                                         upcasted_na=upcasted_na)
                 for ju in join_units]

    if len(to_concat) == 1:
        # Only one block, nothing to concatenate.
        concat_values = to_concat[0]
        if copy and concat_values.base is not None:
            concat_values = concat_values.copy()
    else:
        concat_values = com._concat_compat(to_concat, axis=concat_axis)

    return concat_values
