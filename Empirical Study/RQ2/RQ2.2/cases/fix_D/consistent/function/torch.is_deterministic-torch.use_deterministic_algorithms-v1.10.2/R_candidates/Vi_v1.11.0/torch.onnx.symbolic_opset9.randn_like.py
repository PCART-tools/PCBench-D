def randn_like(g, self, dtype, layout=None, device=None, pin_memory=False, memory_format=None):
    dtype = sym_help._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = ScalarType.FLOAT
    return g.op("RandomNormalLike", self, dtype_i=sym_help.scalar_type_to_onnx[dtype])
