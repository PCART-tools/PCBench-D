@_onnx_symbolic("aten::numpy_T")
@symbolic_helper.quantized_args(True)
def numpy_T(g: jit_utils.GraphContext, input):
    ndim = symbolic_helper._get_tensor_rank(input)
    assert ndim is not None
    perm = list(reversed(range(0, ndim)))
    return g.op("Transpose", input, perm_i=perm)
