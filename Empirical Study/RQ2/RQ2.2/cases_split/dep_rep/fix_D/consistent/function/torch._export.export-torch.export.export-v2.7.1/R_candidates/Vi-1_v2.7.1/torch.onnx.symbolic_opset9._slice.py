@symbolic_helper.quantized_args(True)
def _slice(g: jit_utils.GraphContext, input, axes, starts, ends):
    assert len(starts) == len(ends)
    if len(starts) == 1 and starts[0] == 0 and ends[0] == _constants.INT64_MAX:
        return input
    return g.op("Slice", input, axes_i=axes, starts_i=starts, ends_i=ends)
