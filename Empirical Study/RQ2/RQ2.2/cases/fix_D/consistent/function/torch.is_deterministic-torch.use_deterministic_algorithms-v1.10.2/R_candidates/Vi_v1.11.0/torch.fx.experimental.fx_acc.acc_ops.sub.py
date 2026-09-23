@register_acc_op_properties(AccOpProperty.pointwise)
@register_acc_op_mapping(op_and_target=("call_function", operator.sub))
@register_acc_op
def sub(*, input, other):
    return input - other
