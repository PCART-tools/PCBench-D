@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def max_full_reduce(*, input):
    return torch.max(input=input)
