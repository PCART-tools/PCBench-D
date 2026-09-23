@register_acc_op_mapping(op_and_target=("call_function", operator.truediv))
@register_acc_op
def div(*, input, other):
    return input / other
