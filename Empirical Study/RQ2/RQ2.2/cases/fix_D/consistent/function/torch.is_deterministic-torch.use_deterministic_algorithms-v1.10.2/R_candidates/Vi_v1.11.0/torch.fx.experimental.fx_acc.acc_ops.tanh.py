@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.tanh))
@register_acc_op_mapping(op_and_target=("call_method", "tanh"))
@register_acc_op
def tanh(*, input):
    return torch.tanh(input=input)
