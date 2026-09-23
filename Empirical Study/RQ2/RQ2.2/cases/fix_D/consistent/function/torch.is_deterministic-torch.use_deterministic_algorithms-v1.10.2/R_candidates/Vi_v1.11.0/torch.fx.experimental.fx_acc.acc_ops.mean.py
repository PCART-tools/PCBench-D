@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def mean(*, input, dim=None, keepdim=False, dtype=None):
    if dim is not None:
        return torch.mean(input, dim=dim, keepdim=keepdim, dtype=dtype)
    else:
        return input.mean(dtype=dtype)
