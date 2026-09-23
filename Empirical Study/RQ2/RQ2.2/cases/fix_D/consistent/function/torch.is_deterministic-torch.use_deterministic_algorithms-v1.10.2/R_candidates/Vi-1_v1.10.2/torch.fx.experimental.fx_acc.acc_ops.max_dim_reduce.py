@register_acc_op
def max_dim_reduce(*, input, dim=None, keepdim=False):
    return torch.max(**locals())
