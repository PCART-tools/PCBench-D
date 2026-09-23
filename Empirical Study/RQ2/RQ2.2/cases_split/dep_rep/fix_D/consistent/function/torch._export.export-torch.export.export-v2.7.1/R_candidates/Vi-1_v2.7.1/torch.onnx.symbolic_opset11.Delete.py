@_onnx_symbolic("aten::Delete")
def Delete(g: jit_utils.GraphContext, tensor_list, dim):
    return g.op("SequenceErase", tensor_list, dim)
