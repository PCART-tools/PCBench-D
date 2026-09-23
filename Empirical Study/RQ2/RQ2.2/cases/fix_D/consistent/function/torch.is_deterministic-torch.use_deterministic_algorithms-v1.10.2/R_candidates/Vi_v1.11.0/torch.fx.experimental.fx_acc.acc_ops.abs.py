@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.abs))
@register_acc_op
def abs(*, input):
    return torch.abs(input=input)
