def index_put(g, self, indices_list_value, values, accumulate):
    if sym_help._is_packed_list(indices_list_value):
        indices_list = sym_help._unpack_list(indices_list_value)
    else:
        indices_list = [indices_list_value]
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        args = [self] + indices_list + [values, accumulate]
        return g.op("ATen", *args, operator_s="index_put")

    accumulate = sym_help._parse_arg(accumulate, "b")

    if len(indices_list) == 0:
        if accumulate:
            return add(g, self, values)
        else:
            return values
    else:
        sym_help._onnx_opset_unsupported("index_put", 9, 11)
