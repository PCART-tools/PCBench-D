@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.tan))
@register_acc_op
def tan(*, input):
    return torch.tan(input=input)
