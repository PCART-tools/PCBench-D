@_onnx_symbolic("aten::conv_transpose1d")
@symbolic_helper.parse_args("v", "v", "v", "is", "is", "is", "i", "is")
def conv_transpose1d(
    g: jit_utils.GraphContext,
    input,
    weight,
    bias,
    stride,
    padding,
    output_padding,
    groups,
    dilation,
):
    return _convolution(
        g,
        input,
        weight,
        bias,
        stride,
        padding,
        dilation,
        True,
        output_padding,
        groups,
        None,
        None,
        None,
        None,
    )
