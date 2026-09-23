def scalar_tensor(g, scalar, dtype, *options):
    dtype = sym_help._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = ScalarType.FLOAT
    scalar = g.op("Cast", scalar, to_i=sym_help.scalar_type_to_onnx[dtype])
    return scalar
