@_onnx_symbolic("aten::constant_pad_nd")
def constant_pad_nd(g: jit_utils.GraphContext, input, padding, value=None):
    mode = "constant"
    value = symbolic_helper._maybe_get_scalar(value)
    value = symbolic_helper._if_scalar_type_as(value, input)
    pad = _prepare_onnx_paddings(g, input, padding)
    return g.op("Pad", input, pad, value, mode_s=mode)
