@_onnx_symbolic("aten::__interpolate")
@symbolic_helper.quantized_args(True, False, False, False, False, False, False)
def __interpolate(
    g: jit_utils.GraphContext,
    input,
    size,
    scale_factor,
    mode,
    align_corners,
    recompute_scale_factor,
    antialias,
):
    return symbolic_helper.__interpolate_helper(
        g, input, size, scale_factor, mode, align_corners, recompute_scale_factor
    )
