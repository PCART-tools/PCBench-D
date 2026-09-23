@register_acc_op_mapping(
    op_and_target=("call_function", nn.functional.adaptive_avg_pool2d)
)
@register_acc_op
def adaptive_avg_pool2d(*, input, output_size):
    return nn.functional.adaptive_avg_pool2d(**locals())
