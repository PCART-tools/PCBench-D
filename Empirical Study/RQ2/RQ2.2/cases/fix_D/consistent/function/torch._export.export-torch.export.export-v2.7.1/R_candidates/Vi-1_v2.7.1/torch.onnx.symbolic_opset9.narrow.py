@_onnx_symbolic("aten::narrow")
@symbolic_helper.parse_args("v", "i", "i", "i")
def narrow(g: jit_utils.GraphContext, input, dim, start, length):
    return symbolic_helper._slice_helper(
        g, input, axes=[dim], starts=[start], ends=[start + length]
    )
