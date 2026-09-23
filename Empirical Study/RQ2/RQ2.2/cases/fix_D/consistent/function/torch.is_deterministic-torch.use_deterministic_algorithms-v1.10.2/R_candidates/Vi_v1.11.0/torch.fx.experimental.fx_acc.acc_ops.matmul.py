@register_acc_op_mapping(
    op_and_target=("call_function", torch.bmm),
    arg_replacement_tuples=[
        ("input", "input"),
        ("mat2", "other"),
    ],
)
@register_acc_op_mapping(op_and_target=("call_function", torch.matmul))
@register_acc_op
def matmul(*, input, other):
    return torch.matmul(input=input, other=other)
