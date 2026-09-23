@_onnx_symbolic("aten::numel")
def numel(g: jit_utils.GraphContext, self):
    return symbolic_helper._numel_helper(g, self)
