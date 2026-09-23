@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.gelu))
@register_acc_op_mapping(op_and_target=("call_method", "gelu"))
@register_acc_op
def gelu(*, input):
    return torch.nn.functional.gelu(input=input)
