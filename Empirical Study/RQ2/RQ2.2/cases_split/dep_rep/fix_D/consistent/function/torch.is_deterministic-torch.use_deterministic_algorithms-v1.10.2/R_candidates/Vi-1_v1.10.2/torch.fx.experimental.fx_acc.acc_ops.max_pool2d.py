@register_acc_op_mapping(op_and_target=("call_function", nn.functional.max_pool2d))
@register_acc_op
def max_pool2d(
    *, input, kernel_size, stride, padding, dilation, ceil_mode, return_indices
):
    return nn.functional.max_pool2d(**locals())
