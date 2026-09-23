@_onnx_symbolic("aten::zero")
def zero(g: jit_utils.GraphContext, self):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    return zeros_like(g, self, self_dtype)
