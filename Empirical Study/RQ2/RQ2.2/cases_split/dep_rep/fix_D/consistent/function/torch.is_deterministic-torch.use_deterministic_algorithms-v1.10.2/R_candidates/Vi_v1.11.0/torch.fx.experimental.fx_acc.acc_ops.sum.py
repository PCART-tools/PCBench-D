@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def sum(*, input, dim=None, keepdim=False, dtype=None):
    if dim is not None:
        return torch.sum(input, dim=dim, keepdim=keepdim, dtype=dtype)
    else:
        return input.sum(dtype=dtype)
