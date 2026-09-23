@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def max_dim_reduce(*, input, dim=None, keepdim=False):
    return torch.max(input=input, dim=dim, keepdim=keepdim)
