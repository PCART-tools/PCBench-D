@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_method", "dequantize"))
@register_acc_op_mapping(op_and_target=("call_function", torch.dequantize))
@register_acc_op
def dequantize(*, input):
    return torch.dequantize(input)
