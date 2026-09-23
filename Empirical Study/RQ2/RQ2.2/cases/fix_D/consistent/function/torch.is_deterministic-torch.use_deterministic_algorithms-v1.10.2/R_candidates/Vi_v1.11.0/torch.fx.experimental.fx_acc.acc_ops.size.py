@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op
def size(*, input):
    return input.size()
