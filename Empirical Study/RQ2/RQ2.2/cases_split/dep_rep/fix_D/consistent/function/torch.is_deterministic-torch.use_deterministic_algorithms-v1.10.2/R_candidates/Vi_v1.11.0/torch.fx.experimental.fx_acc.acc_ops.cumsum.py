@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.cumsum))
@register_acc_op_mapping(op_and_target=("call_method", "cumsum"))
@register_acc_op
def cumsum(*, input, dim, dtype=None):
    return torch.cumsum(input=input, dim=dim, dtype=dtype)
