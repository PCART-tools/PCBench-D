@register_acc_op_mapping(op_and_target=("call_function", torch.exp))
@register_acc_op
def exp(*, input):
    return torch.exp(**locals())
