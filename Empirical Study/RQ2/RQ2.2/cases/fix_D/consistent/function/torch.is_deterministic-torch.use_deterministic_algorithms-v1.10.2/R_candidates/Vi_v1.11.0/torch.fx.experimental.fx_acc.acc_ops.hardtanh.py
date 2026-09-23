@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_function", nn.functional.hardtanh),
)
@register_acc_op
def hardtanh(*, input, min_val=-1.0, max_val=1.0):
    return nn.functional.hardtanh(input=input, min_val=min_val, max_val=max_val)
