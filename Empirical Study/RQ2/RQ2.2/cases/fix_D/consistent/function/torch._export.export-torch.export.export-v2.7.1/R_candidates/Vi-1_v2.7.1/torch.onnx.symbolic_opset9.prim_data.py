@_onnx_symbolic("prim::data")
def prim_data(g: jit_utils.GraphContext, self):
    return self
