def _slice(g, input, axes, starts, ends, steps=None, dynamic_slice=False):
    if dynamic_slice:
        starts = sym_help._unsqueeze_helper(g, starts, [0])
        ends = sym_help._unsqueeze_helper(g, ends, [0])
        if isinstance(axes, int):
            axes = g.op("Constant", value_t=torch.tensor(axes))
        axes = sym_help._unsqueeze_helper(g, axes, [0])
    else:
        assert len(starts) == len(ends)
        assert len(starts) == len(axes)
        assert steps is None or len(starts) == len(steps)
        if len(starts) == 1 and starts[0] == 0 and ends[0] == 9223372036854775807\
           and (steps is None or (len(steps) == 1 and steps[0] == 1)):
            return input
        axes = g.op("Constant", value_t=torch.tensor(axes))
        starts = g.op("Constant", value_t=torch.tensor(starts))
        ends = g.op("Constant", value_t=torch.tensor(ends))
    if steps is None:
        return g.op("Slice", input, starts, ends, axes)
    steps = g.op("Constant", value_t=torch.tensor(steps))
    return g.op("Slice", input, starts, ends, axes, steps)
