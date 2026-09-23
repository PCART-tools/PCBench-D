@register_acc_op_mapping(op_and_target=("call_function", nn.functional.avg_pool2d))
@register_acc_op
def avg_pool2d(
    *,
    input,
    kernel_size,
    stride,
    padding,
    ceil_mode,
    count_include_pad,
    divisor_override,
):
    return nn.functional.avg_pool2d(
        input=input,
        kernel_size=kernel_size,
        stride=stride,
        padding=padding,
        ceil_mode=ceil_mode,
        count_include_pad=count_include_pad,
        divisor_override=divisor_override,
    )
