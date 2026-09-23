@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", nn.functional.hardsigmoid))
@register_acc_op
def hardsigmoid(*, input):
    return nn.functional.hardsigmoid(input)
