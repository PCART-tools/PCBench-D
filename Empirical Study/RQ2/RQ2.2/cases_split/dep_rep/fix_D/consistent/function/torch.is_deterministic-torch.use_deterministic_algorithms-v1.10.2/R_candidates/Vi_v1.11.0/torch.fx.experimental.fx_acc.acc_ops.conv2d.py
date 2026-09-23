@register_acc_op_mapping(op_and_target=("call_function", torch.conv2d))
@register_acc_op
def conv2d(*, input, weight, bias, stride, padding, dilation, groups):
    return nn.functional.conv2d(
        input=input,
        weight=weight,
        bias=bias,
        stride=stride,
        padding=padding,
        dilation=dilation,
        groups=groups,
    )
