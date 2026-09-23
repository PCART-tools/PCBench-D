@register_acc_op
def max_full_reduce(*, input):
    return torch.max(**locals())
