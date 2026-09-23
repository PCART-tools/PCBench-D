@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_method", "unsqueeze"))
@register_acc_op_mapping(op_and_target=("call_function", torch.unsqueeze))
@register_acc_op
def unsqueeze(*, input, dim):
    return torch.unsqueeze(input=input, dim=dim)
