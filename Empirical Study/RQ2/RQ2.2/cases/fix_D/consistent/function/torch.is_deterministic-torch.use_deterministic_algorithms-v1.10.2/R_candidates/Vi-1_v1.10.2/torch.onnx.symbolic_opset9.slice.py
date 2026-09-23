def slice(g, self, *args):
    if len(args) == 4:
        # aten::slice(Tensor self, int dim, int start, int end, int step) -> Tensor
        dim, start, end, step = args
        step = _parse_arg(step, "i")
        if step != 1:
            raise RuntimeError("step!=1 is currently not supported")
        is_start_none = start.node().kind() == "prim::Constant" and start.type().kind() == 'NoneType'
        is_end_none = end.node().kind() == "prim::Constant" and end.type().kind() == 'NoneType'
        is_start_onnx_const = start.node().kind() == 'onnx::Constant'
        is_end_onnx_const = end.node().kind() == 'onnx::Constant'
        if ((not is_start_none) and (not is_start_onnx_const)) or \
           ((not is_end_none) and (not is_end_onnx_const)) or \
           dim.node().kind() != 'onnx::Constant':
            if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX:
                raise RuntimeError("Unsupported: ONNX export of Slice with dynamic inputs. DynamicSlice "
                                   "is a deprecated experimental op. Please use statically allocated "
                                   "variables or export to a higher opset version.")
            else:
                start_unsqueezed = sym_help._unsqueeze_helper(g, start, [0])
                end_unsqueezed = sym_help._unsqueeze_helper(g, end, [0])
                dim_unsqueezed = sym_help._unsqueeze_helper(g, dim, [0])
                return g.op("DynamicSlice", self, start_unsqueezed, end_unsqueezed, dim_unsqueezed)
        else:
            start = 0 if is_start_none else _parse_arg(start, 'i')
            end = 9223372036854775807 if is_end_none else _parse_arg(end, 'i')
            dim = _parse_arg(dim, 'i')
            return sym_help._slice_helper(g, self, axes=[dim], starts=[start], ends=[end])
    elif len(args) == 3:
        # aten::slice(t[] l, int start, int end, int step) -> t[]
        start, end, step = args
        dim = 0
        is_start_none = start.node().kind() == "prim::Constant" and start.type().kind() == 'NoneType'
        is_end_none = end.node().kind() == "prim::Constant" and end.type().kind() == 'NoneType'
        start = 0 if is_start_none else _parse_arg(start, 'i')
        end = 9223372036854775807 if is_end_none else _parse_arg(end, 'i')
        return sym_help._slice_helper(g, self, axes=[dim], starts=[start], ends=[end])
    else:
        raise NotImplementedError("Unknown aten::slice signature")
