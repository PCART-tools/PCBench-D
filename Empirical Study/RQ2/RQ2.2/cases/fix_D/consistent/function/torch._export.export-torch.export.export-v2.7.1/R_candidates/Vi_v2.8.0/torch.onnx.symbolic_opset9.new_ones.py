@_onnx_symbolic("aten::new_ones")
def new_ones(
    g: jit_utils.GraphContext, self, sizes, dtype, layout, device, pin_memory=False
):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    if symbolic_helper._is_none(dtype) and self_dtype is not None:
        dtype = self_dtype
    return ones(g, sizes, dtype, layout, device, pin_memory)
