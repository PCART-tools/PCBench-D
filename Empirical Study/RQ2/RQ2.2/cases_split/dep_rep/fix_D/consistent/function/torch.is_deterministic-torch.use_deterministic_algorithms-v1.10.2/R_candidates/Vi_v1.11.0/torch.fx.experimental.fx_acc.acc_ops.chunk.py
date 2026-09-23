@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(op_and_target=("call_function", torch.chunk))
@register_acc_op_mapping(op_and_target=("call_method", "chunk"))
@register_acc_op
def chunk(*, input, chunks, dim=0):
    return torch.chunk(input=input, chunks=chunks, dim=dim)
