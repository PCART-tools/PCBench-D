def prim_dtype(g, self):
    dtype = sym_help._try_get_scalar_type(self)
    if dtype is None:
        dtype = "Float"
    dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    return g.op("Constant", value_t=torch.tensor(dtype))
