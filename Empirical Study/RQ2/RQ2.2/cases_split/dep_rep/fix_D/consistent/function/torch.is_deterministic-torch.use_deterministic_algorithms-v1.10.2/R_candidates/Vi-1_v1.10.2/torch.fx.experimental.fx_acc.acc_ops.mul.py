@register_acc_op_mapping(op_and_target=("call_function", torch.mul))
@register_acc_op_mapping(op_and_target=("call_function", operator.mul))
@register_acc_op
def mul(*, input, other):
    return input * other
