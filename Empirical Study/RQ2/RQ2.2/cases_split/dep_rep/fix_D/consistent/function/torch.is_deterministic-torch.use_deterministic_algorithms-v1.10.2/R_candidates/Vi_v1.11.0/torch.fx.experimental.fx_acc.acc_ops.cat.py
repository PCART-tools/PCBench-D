@register_acc_op_mapping(op_and_target=("call_function", torch.cat))
@register_acc_op
def cat(*, tensors, dim):
    return torch.cat(tensors=tensors, dim=dim)
