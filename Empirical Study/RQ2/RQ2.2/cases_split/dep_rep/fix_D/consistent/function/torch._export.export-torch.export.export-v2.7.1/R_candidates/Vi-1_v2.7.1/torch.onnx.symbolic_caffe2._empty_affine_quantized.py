@symbolic_helper.parse_args("v", "t", "t", "t", "t", "t", "t", "t")
def _empty_affine_quantized(
    g: jit_utils.GraphContext,
    input,
    shape,
    scale,
    zero_point,
    dtype,
    pin_memory,
    memory_format,
    layout,
):
    return input
