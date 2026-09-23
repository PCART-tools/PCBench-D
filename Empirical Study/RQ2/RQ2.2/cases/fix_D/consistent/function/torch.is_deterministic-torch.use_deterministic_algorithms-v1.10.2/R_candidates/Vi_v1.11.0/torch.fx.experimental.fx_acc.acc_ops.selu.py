@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.selu))
@register_acc_op
def selu(*, input, inplace=False):
    return nn.functional.selu(input=input, inplace=inplace)
