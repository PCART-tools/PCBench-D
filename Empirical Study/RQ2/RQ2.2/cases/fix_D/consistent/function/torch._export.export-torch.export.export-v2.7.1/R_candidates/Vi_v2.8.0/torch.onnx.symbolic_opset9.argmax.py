@_onnx_symbolic("aten::argmax")
@symbolic_helper.parse_args("v", "v", "b")
def argmax(
    g: jit_utils.GraphContext,
    input: torch._C.Value,
    dim: torch._C.Value,
    keepdim: bool,
):
    return symbolic_helper._argmin_argmax_helper(g, input, dim, keepdim, "ArgMax")
