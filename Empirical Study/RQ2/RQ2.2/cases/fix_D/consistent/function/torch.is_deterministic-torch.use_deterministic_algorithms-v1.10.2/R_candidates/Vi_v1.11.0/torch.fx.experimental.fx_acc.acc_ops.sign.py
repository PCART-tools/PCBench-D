@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.sign))
@register_acc_op
def sign(*, input):
    return torch.sign(input)
