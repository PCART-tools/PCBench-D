@register_acc_op_mapping(op_and_target=("call_function", torch.linalg.norm))
@register_acc_op
def linalg_norm(*, input, ord, dim, keepdim):
    return torch.linalg.norm(**locals())
