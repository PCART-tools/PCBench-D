@parse_args("v", "v")
def fill(g, self, value):
    dtype = self.type().scalarType()
    if dtype is None:
        dtype = ScalarType.FLOAT
    else:
        dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])

    return full_like(g, self, value, dtype)
