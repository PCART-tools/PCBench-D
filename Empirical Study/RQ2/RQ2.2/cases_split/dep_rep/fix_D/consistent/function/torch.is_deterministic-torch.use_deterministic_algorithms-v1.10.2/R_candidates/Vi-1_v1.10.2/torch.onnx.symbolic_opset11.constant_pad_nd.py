def constant_pad_nd(g, input, padding, value=None):
    mode = "constant"
    value = sym_help._maybe_get_scalar(value)
    value = sym_help._if_scalar_type_as(g, value, input)
    pad = _prepare_onnx_paddings(g, input, padding)
    return g.op("Pad", input, pad, value, mode_s=mode)
