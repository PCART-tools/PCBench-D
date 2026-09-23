def _slice(g, input, axes, starts, ends):
    assert len(starts) == len(ends)
    if len(starts) == 1 and starts[0] == 0 and ends[0] == 9223372036854775807:
        return input
    return g.op("Slice", input, axes_i=axes, starts_i=starts, ends_i=ends)
