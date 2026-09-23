@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.softsign))
@register_acc_op
def softsign(*, input):
    return nn.functional.softsign(input=input)
