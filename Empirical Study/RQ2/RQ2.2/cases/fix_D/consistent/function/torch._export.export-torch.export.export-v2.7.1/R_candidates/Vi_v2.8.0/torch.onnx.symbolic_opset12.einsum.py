@_onnx_symbolic("aten::einsum")
@symbolic_helper.parse_args("s", "v", "is")
def einsum(g: jit_utils.GraphContext, equation, tensor_list, path=None):
    tensors = symbolic_helper._unpack_list(tensor_list)
    return _einsum_helper(g, equation, tensors)
