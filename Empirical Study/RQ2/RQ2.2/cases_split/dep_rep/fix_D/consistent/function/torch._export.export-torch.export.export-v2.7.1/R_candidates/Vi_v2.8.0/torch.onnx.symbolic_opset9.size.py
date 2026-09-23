@_onnx_symbolic("aten::size")
@symbolic_helper.quantized_args(True, quantize_output=False)
def size(g: jit_utils.GraphContext, self, dim=None):
    if dim is None:
        return g.op("Shape", self)
    if symbolic_helper._maybe_get_const(dim, "i") < 0:
        rank = symbolic_helper._get_tensor_rank(self)
        if rank is not None:
            dim = symbolic_helper._maybe_get_const(dim, "i") + rank
            dim = g.op("Constant", value_t=torch.tensor(dim))
    return symbolic_helper._size_helper(g, self, dim)
