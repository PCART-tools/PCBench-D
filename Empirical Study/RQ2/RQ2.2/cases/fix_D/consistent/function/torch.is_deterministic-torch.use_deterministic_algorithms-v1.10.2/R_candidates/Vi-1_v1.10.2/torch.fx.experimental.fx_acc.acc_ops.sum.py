@register_acc_op
def sum(*, input, dim=None, keepdim=False, dtype=None):
    if dim is not None:
        return torch.sum(**locals())
    else:
        return input.sum(dtype=dtype)
