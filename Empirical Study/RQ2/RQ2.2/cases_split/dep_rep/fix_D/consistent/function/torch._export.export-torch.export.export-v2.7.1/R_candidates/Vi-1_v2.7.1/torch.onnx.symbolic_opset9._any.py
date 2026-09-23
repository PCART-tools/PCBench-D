@_onnx_symbolic("aten::any")
def _any(g: jit_utils.GraphContext, *args):
    # aten::any(Tensor self)
    if len(args) == 1:
        input = args[0]
        dim, keepdim = None, 0
    # aten::any(Tensor self, int[]? dim, bool keepdim)
    else:
        input, dim, keepdim = args
        # Can be int list or single int
        dim = symbolic_helper._parse_arg(dim, "t")
        dim = [int(d) for d in dim.view(-1)]
        keepdim = symbolic_helper._parse_arg(keepdim, "i")
    input = g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.INT64)
    input_sum = symbolic_helper._reducesum_helper(
        g, input, axes_i=dim, keepdims_i=keepdim
    )
    return gt(g, input_sum, g.op("Constant", value_t=torch.tensor(0, dtype=torch.long)))
