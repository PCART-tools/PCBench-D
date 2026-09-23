@_onnx_symbolic("aten::argsort")
@symbolic_helper.parse_args("v", "i", "i", "none")
def argsort(g: jit_utils.GraphContext, self, dim, decending, out=None):
    _, indices = symbolic_helper._sort_helper(
        g, self, dim, decending=decending, out=out
    )
    return indices
