def randn(g, shapes, dtype, *options):
    dtype = sym_help._get_const(dtype, "i", "dtype")
    if dtype is None:
        dtype = 6  # float
    shape = sym_help._maybe_get_const(shapes, "is")
    if sym_help._is_value(shape):
        shape_const = g.op("ConstantOfShape", shapes,
                           value_t=torch.tensor([0], dtype=sym_help.scalar_type_to_pytorch_type[6]))
        return g.op("RandomNormalLike", shape_const, dtype_i=sym_help.scalar_type_to_onnx[dtype])
    return g.op("RandomNormal", shape_i=shape)
