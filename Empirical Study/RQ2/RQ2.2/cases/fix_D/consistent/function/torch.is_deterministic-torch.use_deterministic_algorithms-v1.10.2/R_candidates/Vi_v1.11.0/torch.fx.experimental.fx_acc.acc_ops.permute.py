@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_method", "permute"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("*", "permutation"),
    ],
)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.permute),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dims", "permutation"),
    ],
)
@register_acc_op
def permute(*, input, permutation):
    return input.permute(*permutation)
