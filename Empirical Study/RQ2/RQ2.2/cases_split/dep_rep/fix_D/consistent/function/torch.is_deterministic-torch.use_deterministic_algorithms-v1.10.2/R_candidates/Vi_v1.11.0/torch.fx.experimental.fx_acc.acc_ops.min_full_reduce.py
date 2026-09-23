@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def min_full_reduce(*, input):
    return torch.min(input=input)
