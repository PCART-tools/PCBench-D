@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.sin))
@register_acc_op
def sin(*, input):
    return torch.sin(input=input)
