@_onnx_symbolic("aten::cat")
@symbolic_helper.quantized_args(True)
def cat(g: jit_utils.GraphContext, tensor_list, dim):
    if symbolic_helper._is_packed_list(tensor_list):
        return opset9.cat(g, tensor_list, dim)
    else:
        dim = symbolic_helper._get_const(dim, "i", "dim")
        return g.op("ConcatFromSequence", tensor_list, axis_i=dim)
