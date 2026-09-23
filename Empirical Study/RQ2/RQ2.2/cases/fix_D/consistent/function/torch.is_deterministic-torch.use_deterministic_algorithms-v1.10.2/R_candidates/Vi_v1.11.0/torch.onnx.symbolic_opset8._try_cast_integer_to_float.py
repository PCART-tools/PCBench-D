def _try_cast_integer_to_float(g, *args):
    floating_scalar_types = ["Half", "Float", "Double"]
    old_type = None
    # Cast the input tensor to Float if its scalarType is known and is not floating number.
    # If casting is performed, return the old scalarType, otherwise return None.
    arg0_type = args[0].type().scalarType()
    if arg0_type is not None:
        old_type = arg0_type
        if old_type not in floating_scalar_types:
            args = tuple(_cast_Float(g, arg, False) for arg in args)
        else:
            return (None,) + args
    else:
        warnings.warn("Only floating datatype is supported for these operators: "
                      "{Greater, Less, MatMul, PRelu, Gemm, Flatten}. This might cause "
                      "the onnx model to be incorrect, if inputs have integer datatypes.")
    return (old_type,) + args
