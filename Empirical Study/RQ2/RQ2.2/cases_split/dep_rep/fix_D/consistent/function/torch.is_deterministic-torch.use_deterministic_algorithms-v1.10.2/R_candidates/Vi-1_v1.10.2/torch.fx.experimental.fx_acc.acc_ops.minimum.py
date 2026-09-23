@register_acc_op_mapping(op_and_target=("call_function", torch.minimum))
@register_acc_op_mapping(op_and_target=("call_method", "minimum"))
@register_acc_op
def minimum(*, input, other):
    return torch.minimum(**locals())
