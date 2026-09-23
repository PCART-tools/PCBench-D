@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.reciprocal))
@register_acc_op
def reciprocal(*, input):
    return torch.reciprocal(input=input)
