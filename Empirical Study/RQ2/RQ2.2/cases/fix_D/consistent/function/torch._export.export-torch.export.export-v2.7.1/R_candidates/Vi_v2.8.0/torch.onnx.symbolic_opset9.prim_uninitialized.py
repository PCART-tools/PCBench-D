@_onnx_symbolic("prim::Uninitialized")
def prim_uninitialized(g: jit_utils.GraphContext, *inputs, **kwargs):
    return None
