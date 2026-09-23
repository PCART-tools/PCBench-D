@register_acc_op_mapping(op_and_target=("call_function", torch.ceil))
@register_acc_op
def ceil(*, input):
    return torch.ceil(**locals())
