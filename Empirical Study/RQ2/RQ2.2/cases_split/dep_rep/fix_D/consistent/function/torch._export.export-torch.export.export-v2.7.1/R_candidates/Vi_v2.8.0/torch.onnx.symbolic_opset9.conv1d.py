@_onnx_symbolic("aten::conv1d")
@symbolic_helper.parse_args("v", "v", "v", "is", "v", "is", "i")
def conv1d(
    g: jit_utils.GraphContext, input, weight, bias, stride, padding, dilation, groups
):
    str_padding = symbolic_helper._parse_arg(padding, "s")
    if str_padding in ["valid", "same"]:
        return _convolution_mode(
            g,
            input,
            weight,
            bias,
            stride,
            str_padding,
            dilation,
            groups,
        )
    else:
        padding = symbolic_helper._parse_arg(padding, "is")
        return _convolution(
            g,
            input,
            weight,
            bias,
            stride,
            padding,
            dilation,
            False,
            (),
            groups,
            None,
            None,
            None,
            None,
        )
