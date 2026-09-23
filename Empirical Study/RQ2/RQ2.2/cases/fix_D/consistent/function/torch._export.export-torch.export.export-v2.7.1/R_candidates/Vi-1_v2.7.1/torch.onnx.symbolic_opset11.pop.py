@_onnx_symbolic("aten::pop")
def pop(g: jit_utils.GraphContext, tensor_list, dim):
    return g.op("SequenceErase", tensor_list, dim)
