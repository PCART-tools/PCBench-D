@register_acc_op_mapping(op_and_target=("call_function", torch.topk))
@register_acc_op
def topk(*, input, k, dim, largest, sorted):
    return torch.topk(**locals())
