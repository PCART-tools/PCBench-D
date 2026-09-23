def slice(g, self, *args):
    if len(args) == 4:
        # aten::slice(Tensor self, int dim, int? start=None, int? end=None, int step=1) -> Tensor
        dim, start, end, step = args
    elif len(args) == 3:
        # aten::slice(t[] l, int? start=None, int? end=None, int step=1) -> t[]
        start, end, step = args
        dim = 0
    else:
        raise NotImplementedError("Unknown aten::slice signature")
    is_start_none = start.node().kind() == "prim::Constant" and start.type().kind() == "NoneType"
    is_end_none = end.node().kind() == "prim::Constant" and end.type().kind() == "NoneType"
    is_start_onnx_const = start.node().kind() == "onnx::Constant"
    is_end_onnx_const = end.node().kind() == "onnx::Constant"
    step = sym_help._parse_arg(step, "i")
    if (not is_start_none and not is_start_onnx_const) or \
       (not isinstance(end, int) and not is_end_none and not is_end_onnx_const) or \
       (not isinstance(dim, int) and dim.node().kind() != "onnx::Constant"):
        dynamic_slice = True
        if is_start_none:
            start = g.op("Constant", value_t=torch.tensor(0))
        if is_end_none:
            end = g.op("Constant", value_t=torch.tensor(9223372036854775807))
    else:
        start = [0 if is_start_none else sym_help._parse_arg(start, "i")]
        end = [9223372036854775807 if is_end_none else sym_help._parse_arg(end, "i")]
        dim = [sym_help._parse_arg(dim, "i")]
        dynamic_slice = False
    return sym_help._slice_helper(g, self, axes=dim, starts=start, ends=end, steps=[step], dynamic_slice=dynamic_slice)
