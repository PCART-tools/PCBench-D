@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_method", "squeeze"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim", this_arg_is_optional),
    ],
)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.squeeze),
    arg_replacement_tuples=[
        ("input", "input"),
        ("dim", "dim", this_arg_is_optional),
    ],
)
@register_acc_op
def squeeze(*, input, dim=None):
    if dim is None:
        return input.squeeze()
    return input.squeeze(dim=dim)
