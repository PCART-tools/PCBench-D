@register_acc_op
def tuple_construct(*, tensors):
    return tuple(tensors)
