@parse_args("v", "f", "f")
def hardtanh(g, self, min_val, max_val):
    dtype = self.type().scalarType()
    if dtype is None:
        dtype = 6  # float
    else:
        dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    min_val = g.op("Constant", value_t=torch.tensor(min_val, dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
    max_val = g.op("Constant", value_t=torch.tensor(max_val, dtype=sym_help.scalar_type_to_pytorch_type[dtype]))
    return g.op("Clip", self, min_val, max_val)
