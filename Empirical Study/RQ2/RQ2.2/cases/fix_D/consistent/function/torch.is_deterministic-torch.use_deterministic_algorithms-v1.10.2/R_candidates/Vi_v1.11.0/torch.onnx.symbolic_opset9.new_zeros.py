def new_zeros(g, self, sizes, dtype, layout, device, pin_memory=False):
    self_dtype = sym_help._try_get_scalar_type(self)
    if dtype is None and self_dtype is not None:
        dtype = self_dtype
        dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    return zeros(g, sizes, dtype, layout, device, pin_memory)
