def reflection_pad(g, input, padding):
    mode = "reflect"
    padding = _convert_padding_node(padding)
    paddings = _prepare_onnx_paddings(sym_help._get_tensor_rank(input), padding)
    return g.op("Pad", input, pads_i=paddings, mode_s=mode)
