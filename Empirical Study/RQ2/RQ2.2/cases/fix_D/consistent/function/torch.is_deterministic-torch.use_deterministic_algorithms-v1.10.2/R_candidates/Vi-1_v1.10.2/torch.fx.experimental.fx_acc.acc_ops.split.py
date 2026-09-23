@register_acc_op
def split(*, input, split_size, dim):
    return torch.split(input, split_size, dim)
