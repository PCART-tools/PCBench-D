@_onnx_symbolic("aten::reflection_pad1d")
@_onnx_symbolic("aten::reflection_pad2d")
@_onnx_symbolic("aten::reflection_pad3d")
def reflection_pad(g: jit_utils.GraphContext, input, padding):
    mode = "reflect"
    padding = _convert_padding_node(padding)
    paddings = _prepare_onnx_paddings(symbolic_helper._get_tensor_rank(input), padding)
    return symbolic_helper._op_with_optional_float_cast(
        g, "Pad", input, pads_i=paddings, mode_s=mode, opset_before=11
    )
