@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", nn.functional.relu))
@register_acc_op_mapping(
    op_and_target=("call_function", torch.relu),
    arg_replacement_tuples=[("input", "input")],
)
@register_acc_op_mapping(
    op_and_target=("call_method", "relu"),
    arg_replacement_tuples=[("input", "input")],
)
@register_acc_op
def relu(*, input, inplace=False):
    return nn.functional.relu(input=input, inplace=inplace)
