def _consolidate(blocks):
    """
    Merge blocks having same dtype, exclude non-consolidating blocks
    """

    # sort by _can_consolidate, dtype
    gkey = lambda x: x._consolidate_key
    grouper = itertools.groupby(sorted(blocks, key=gkey), gkey)

    new_blocks = []
    for (_can_consolidate, dtype), group_blocks in grouper:
        merged_blocks = _merge_blocks(list(group_blocks), dtype=dtype,
                                      _can_consolidate=_can_consolidate)
        if isinstance(merged_blocks, list):
            new_blocks.extend(merged_blocks)
        else:
            new_blocks.append(merged_blocks)

    return new_blocks
