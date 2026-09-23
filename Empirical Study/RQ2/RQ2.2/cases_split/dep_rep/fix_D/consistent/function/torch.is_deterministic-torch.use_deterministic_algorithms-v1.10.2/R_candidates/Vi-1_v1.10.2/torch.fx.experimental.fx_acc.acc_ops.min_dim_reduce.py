@register_acc_op
def min_dim_reduce(*, input, dim=None, keepdim=False):
    return torch.min(input, dim=dim, keepdim=keepdim)
