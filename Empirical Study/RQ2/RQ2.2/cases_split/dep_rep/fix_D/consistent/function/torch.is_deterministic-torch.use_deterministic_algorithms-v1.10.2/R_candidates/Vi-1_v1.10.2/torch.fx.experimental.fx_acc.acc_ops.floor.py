@register_acc_op_mapping(op_and_target=("call_function", torch.floor))
@register_acc_op
def floor(*, input):
    return torch.floor(**locals())
