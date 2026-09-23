@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.nn.functional.softmax))
@register_acc_op
def softmax(*, input, dim, dtype):
    """
    _stacklevel are ignored here.
    """
    return torch.nn.functional.softmax(input=input, dim=dim, dtype=dtype)
