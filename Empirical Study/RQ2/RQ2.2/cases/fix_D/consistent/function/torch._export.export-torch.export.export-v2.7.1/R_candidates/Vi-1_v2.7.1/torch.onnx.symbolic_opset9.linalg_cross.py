@_onnx_symbolic("aten::linalg_cross")
@symbolic_helper.parse_args("v", "v", "i")
def linalg_cross(g: jit_utils.GraphContext, input, other, dim=-1):
    return cross(g, input, other, dim)
