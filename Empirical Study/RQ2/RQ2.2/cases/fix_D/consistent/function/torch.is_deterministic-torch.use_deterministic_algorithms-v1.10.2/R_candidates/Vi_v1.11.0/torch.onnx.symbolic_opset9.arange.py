def arange(g, *args):
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen", *args, operator_s="arange")

    def _get_arange_dtype(dtype):
        dtype = sym_help._maybe_get_const(dtype, "i")
        return dtype

    def _float_step_convert(range_tensor):
        if sym_help._is_fp(range_tensor):
            range_tensor = g.op("Cast", g.op("Ceil", range_tensor), to_i=sym_help.scalar_type_to_onnx[4])
        return range_tensor

    if len(args) == 2 or len(args) == 5:
        if len(args) == 2:
            # aten::arange(Scalar end, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[1])
        dtype, end, start, step = sym_help._arange_cast_helper(g, end=args[0], dtype=dtype)
        end = sym_help._unsqueeze_helper(g, end, [0])
        range_tensor = _float_step_convert(end)
        arange_tensor = sym_help._squeeze_helper(g, nonzero(g, ones(g, range_tensor, dtype, None, None)), [1])
        return g.op("Cast", arange_tensor, to_i=sym_help.scalar_type_to_onnx[dtype])
    elif len(args) == 4 or len(args) == 7:
        if len(args) == 4:
            # aten::arange(Scalar start, Scalar end, Scalar step, Tensor out)
            dtype = None
        else:
            # aten::arange(Scalar start, Scalar end, Scalar step, ScalarType dtype, Layout, Device, bool pin_memory)
            dtype = _get_arange_dtype(args[3])
        dtype, end, start, step = sym_help._arange_cast_helper(g, start=args[0], end=args[1], step=args[2], dtype=dtype)
        step = sym_help._unsqueeze_helper(g, step, [0])
        end = sym_help._unsqueeze_helper(g, end, [0])
        start = sym_help._unsqueeze_helper(g, start, [0])
        range_tensor = _float_step_convert(g.op("Div", g.op("Sub", end, start), step))
        arange_tensor = sym_help._squeeze_helper(g, nonzero(g, ones(g, range_tensor, None, None, None)), [1])
        arange_tensor = g.op("Add", g.op("Mul", arange_tensor, step), start)
        return g.op("Cast", arange_tensor, to_i=sym_help.scalar_type_to_onnx[dtype])
    elif len(args) == 6:
        # aten::arange(Scalar start, Scalar end, ScalarType dtype, Layout, Device, bool pin_memory)
        dtype = _get_arange_dtype(args[2])
        dtype, end, start, step = sym_help._arange_cast_helper(g, start=args[0], end=args[1], dtype=dtype)
        end = sym_help._unsqueeze_helper(g, end, [0])
        start = sym_help._unsqueeze_helper(g, start, [0])
        range_tensor = _float_step_convert(g.op("Sub", end, start))
        arange_tensor = g.op("Add", sym_help._squeeze_helper(g, nonzero(g, ones(g, range_tensor, dtype, *(args[3:]))), [1]), start)
        return g.op("Cast", arange_tensor, to_i=sym_help.scalar_type_to_onnx[dtype])
    else:
        raise NotImplementedError("Unknown aten::arange signature taking " + str(len(args)) + " arguments.")
