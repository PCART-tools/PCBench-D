@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.clamp))
@register_acc_op_mapping(op_and_target=("call_method", "clamp"))
@register_acc_op
def clamp(*, input, min=None, max=None):
    return torch.clamp(input=input, min=min, max=max)
