@register_acc_op_mapping(op_and_target=("call_function", torch.sinh))
@register_acc_op
def sinh(*, input):
    return torch.sinh(**locals())
