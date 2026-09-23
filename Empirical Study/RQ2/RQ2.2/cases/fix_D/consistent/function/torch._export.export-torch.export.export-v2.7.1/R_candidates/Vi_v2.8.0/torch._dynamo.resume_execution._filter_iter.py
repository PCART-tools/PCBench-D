def _filter_iter(l1, l2, cond):
    """
    Two-pointer conditional filter.
    e.g. _filter_iter(insts, sorted_offsets, lambda i, o: i.offset == o)
    returns the instructions with offsets in sorted_offsets
    """
    it = iter(l2)
    res: list[Instruction] = []
    try:
        cur = next(it)
        for val in l1:
            if cond(val, cur):
                res.append(val)
                cur = next(it)
    except StopIteration:
        pass
    return res
