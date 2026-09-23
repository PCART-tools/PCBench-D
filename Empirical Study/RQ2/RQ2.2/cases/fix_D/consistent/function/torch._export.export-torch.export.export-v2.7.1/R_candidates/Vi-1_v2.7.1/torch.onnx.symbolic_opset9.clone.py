@_onnx_symbolic("aten::clone")
# ignore clone operators that are inserted by PyTorch autograd
def clone(g: jit_utils.GraphContext, input, unused_memory_format):
    return input
