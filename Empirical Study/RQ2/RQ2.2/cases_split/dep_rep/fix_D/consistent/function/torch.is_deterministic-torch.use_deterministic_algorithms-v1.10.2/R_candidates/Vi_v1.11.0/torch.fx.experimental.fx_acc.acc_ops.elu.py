@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.elu))
@register_acc_op
def elu(*, input, alpha=1.0, inplace=False):
    return nn.functional.elu(input=input, alpha=alpha, inplace=inplace)
