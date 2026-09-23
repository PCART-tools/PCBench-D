@register_acc_op_mapping(op_and_target=("call_function", torch.maximum))
@register_acc_op_mapping(op_and_target=("call_method", "maximum"))
@register_acc_op
def maximum(*, input, other):
    return torch.maximum(**locals())
