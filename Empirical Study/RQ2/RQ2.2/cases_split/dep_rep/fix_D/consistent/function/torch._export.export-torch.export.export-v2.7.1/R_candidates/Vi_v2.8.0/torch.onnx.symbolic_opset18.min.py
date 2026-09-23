@_onnx_symbolic("aten::min")
# TODO(justinchuby): Support multiple quantized args in output
def min(g: jit_utils.GraphContext, self, dim_or_y=None, keepdim=None):
    return symbolic_helper._min_helper(g, self, dim_or_y, keepdim)
