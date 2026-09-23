@register_acc_op_properties(AccOpProperty.pointwise)
@register_acc_op_mapping(op_and_target=("call_function", torch.maximum))
@register_acc_op_mapping(op_and_target=("call_method", "maximum"))
@register_acc_op
def maximum(*, input, other):
    return torch.maximum(input=input, other=other)
