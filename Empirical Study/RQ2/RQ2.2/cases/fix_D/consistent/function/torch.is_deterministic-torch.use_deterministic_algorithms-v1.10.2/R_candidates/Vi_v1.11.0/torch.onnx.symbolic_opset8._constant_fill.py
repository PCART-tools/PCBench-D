def _constant_fill(g, sizes, dtype, const_value):
    if dtype is None:
        dtype = ScalarType.FLOAT
    if not sym_help.scalar_type_to_pytorch_type[dtype].is_floating_point:
        result = g.op(
            "ConstantFill", sizes, dtype_i=sym_help.cast_pytorch_to_onnx["Float"], input_as_shape_i=1, value_f=const_value)
        return sym_help._cast_func_template(sym_help.scalar_type_to_onnx[dtype], g, result, None)
    else:
        return g.op("ConstantFill", sizes, dtype_i=sym_help.scalar_type_to_onnx[dtype], input_as_shape_i=1, value_f=const_value)
