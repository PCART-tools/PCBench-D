@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.nn.functional.leaky_relu)
)
@register_acc_op
def leaky_relu(*, input, negative_slope=0.01, inplace=False):
    return nn.functional.leaky_relu(
        input=input, negative_slope=negative_slope, inplace=inplace
    )
