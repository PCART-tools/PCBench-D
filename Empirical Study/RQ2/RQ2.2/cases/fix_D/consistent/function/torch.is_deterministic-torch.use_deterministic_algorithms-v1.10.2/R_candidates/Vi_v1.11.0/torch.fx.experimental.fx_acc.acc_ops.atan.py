@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.atan))
@register_acc_op
def atan(*, input):
    return torch.atan(input=input)
