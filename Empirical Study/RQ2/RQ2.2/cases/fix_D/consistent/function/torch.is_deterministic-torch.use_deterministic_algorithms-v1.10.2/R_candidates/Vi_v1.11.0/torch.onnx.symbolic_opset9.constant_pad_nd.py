def constant_pad_nd(g, input, padding, value):
    mode = "constant"
    try:
        value = sym_help._get_const(value, "f", "value")
    except Exception:
        return sym_help._onnx_opset_unsupported_detailed("Pad", 9, 11, "The value for the padding must be constant")

    padding = _convert_padding_node(padding)
    paddings = _prepare_onnx_paddings(sym_help._get_tensor_rank(input), padding)
    return g.op("Pad", input, pads_i=paddings, mode_s=mode, value_f=value)
