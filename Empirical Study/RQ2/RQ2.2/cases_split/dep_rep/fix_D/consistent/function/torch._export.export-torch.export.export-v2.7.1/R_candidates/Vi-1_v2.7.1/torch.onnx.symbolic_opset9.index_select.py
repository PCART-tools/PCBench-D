@_onnx_symbolic("aten::index_select")
@symbolic_helper.parse_args("v", "i", "v")
def index_select(g: jit_utils.GraphContext, self, dim, index):
    # In case of a scalar index, index_select returns a tensor with the same rank as the input.
    # To match this behavior in ONNX, we make index a 1D tensor so that the following gather
    # also produces a tensor with the same rank as the input.
    return symbolic_helper._select_helper(g, self, dim, index)
