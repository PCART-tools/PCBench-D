@_onnx_symbolic("aten::argmin")
@symbolic_helper.parse_args("v", "v", "b")
def argmin(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMin")
