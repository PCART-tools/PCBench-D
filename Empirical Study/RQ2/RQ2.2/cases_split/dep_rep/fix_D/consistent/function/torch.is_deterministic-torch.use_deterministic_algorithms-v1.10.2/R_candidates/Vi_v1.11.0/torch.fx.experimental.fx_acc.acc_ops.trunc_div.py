@register_acc_op_mapping(op_and_target=("call_function", torch.floor_divide))
@register_acc_op_properties(AccOpProperty.pointwise)
@register_acc_op
def trunc_div(*, input, other):
    return torch.div(input, other, rounding_mode="trunc")
