def arange(g, *args):
    def _get_arange_dtype(dtype):
        dtype = sym_help._maybe_get_const(dtype, "i")
        return dtype

    if len(args) == 2 or len(args) == 5:
        if len(args) == 2:
            # aten::arange(Scalar end, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[1])
        type, end, start, step = sym_help._arange_cast_helper(g, end=args[0], dtype=dtype)
        start_default = g.op("Constant", value_t=torch.tensor(0, dtype=sym_help.scalar_type_to_pytorch_type[type]))
        delta_default = g.op("Constant", value_t=torch.tensor(1, dtype=sym_help.scalar_type_to_pytorch_type[type]))
        arange_tensor = g.op("Range", start_default, end, delta_default)
    elif len(args) == 4 or len(args) == 7:
        if len(args) == 4:
            # aten::arange(Scalar start, Scalar end, Scalar step, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar start, Scalar end, Scalar step, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[3])
        type, end, start, step = sym_help._arange_cast_helper(g, start=args[0], end=args[1], step=args[2], dtype=dtype)
        arange_tensor = g.op("Range", start, end, step)
    elif len(args) == 6:
        # aten::arange(Scalar start, Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
        dtype = _get_arange_dtype(args[2])
        type, end, start, step = sym_help._arange_cast_helper(g, start=args[0], end=args[1], dtype=dtype)
        delta_default = g.op("Constant", value_t=torch.tensor(1, dtype=sym_help.scalar_type_to_pytorch_type[type]))
        arange_tensor = g.op("Range", start, end, delta_default)
    else:
        raise NotImplementedError("Unknown aten::arange signature taking " + str(len(args)) + " arguments.")
    return arange_tensor
