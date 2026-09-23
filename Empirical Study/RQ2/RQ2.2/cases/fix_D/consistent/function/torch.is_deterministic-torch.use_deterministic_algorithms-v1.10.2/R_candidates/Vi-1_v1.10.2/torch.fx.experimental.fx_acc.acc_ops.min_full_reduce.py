@register_acc_op
def min_full_reduce(*, input):
    return torch.min(input)
