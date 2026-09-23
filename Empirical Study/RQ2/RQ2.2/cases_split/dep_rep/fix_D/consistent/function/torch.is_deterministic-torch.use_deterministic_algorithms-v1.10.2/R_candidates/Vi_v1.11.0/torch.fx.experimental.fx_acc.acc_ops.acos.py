@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.acos))
@register_acc_op
def acos(*, input):
    return torch.acos(input=input)
