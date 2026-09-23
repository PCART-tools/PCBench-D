@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_method", "tile"))
@register_acc_op_mapping(op_and_target=("call_function", torch.tile))
@register_acc_op
def tile(*, input, dims):
    return torch.tile(input=input, dims=dims)
