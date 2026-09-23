@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_method", "contiguous"))
@register_acc_op
def contiguous(*, input):
    return input.contiguous()
