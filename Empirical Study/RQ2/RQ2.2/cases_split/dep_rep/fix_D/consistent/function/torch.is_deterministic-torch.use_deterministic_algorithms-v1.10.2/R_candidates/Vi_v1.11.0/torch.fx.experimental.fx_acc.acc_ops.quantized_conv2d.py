@register_acc_op_properties(AccOpProperty.quantized)
@register_acc_op
def quantized_conv2d(
    *,
    input,
    weight,
    bias,
    stride,
    padding,
    dilation,
    groups,
    padding_mode,
    acc_out_ty,
):
    qparams = TensorMetadata(*acc_out_ty).qparams
    return torch.nn.quantized.functional.conv2d(
        input=input,
        weight=weight,
        bias=bias,
        stride=stride,
        padding=padding,
        dilation=dilation,
        groups=groups,
        padding_mode=padding_mode,
        scale=qparams["scale"],
        zero_point=qparams["zero_point"],
    )
