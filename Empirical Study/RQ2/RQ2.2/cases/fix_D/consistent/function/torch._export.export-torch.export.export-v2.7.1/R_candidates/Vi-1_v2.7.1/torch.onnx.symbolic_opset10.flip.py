@_onnx_symbolic("aten::flip")
@symbolic_helper.parse_args("v", "is")
def flip(g: jit_utils.GraphContext, input, dims):
    return symbolic_helper._slice_helper(
        g,
        input,
        axes=dims,
        starts=[-1] * len(dims),
        ends=[-_constants.INT64_MAX] * len(dims),
        steps=[-1] * len(dims),
    )
