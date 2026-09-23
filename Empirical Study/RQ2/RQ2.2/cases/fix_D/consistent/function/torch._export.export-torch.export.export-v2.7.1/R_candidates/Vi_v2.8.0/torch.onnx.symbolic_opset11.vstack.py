@_onnx_symbolic("aten::vstack")
def vstack(g: jit_utils.GraphContext, tensor_list: _C.Value):
    tensor_list = atleast_2d(g, tensor_list)
    return g.op("ConcatFromSequence", tensor_list, axis_i=0, new_axis_i=0)
