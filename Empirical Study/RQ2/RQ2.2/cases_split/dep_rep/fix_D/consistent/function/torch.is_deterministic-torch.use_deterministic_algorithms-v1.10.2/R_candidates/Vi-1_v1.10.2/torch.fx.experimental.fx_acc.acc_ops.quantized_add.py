@register_acc_op_mapping(
    op_and_target=("call_function", torch.ops.quantized.add),
    arg_replacement_tuples=[
        ("qa", "input"),
        ("qb", "other"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("scale", "q_scale"),
        ("zero_point", "q_zero_point"),
    ],
)
@register_acc_op
def quantized_add(*, input, other, acc_out_ty=None):
    assert acc_out_ty is not None
    return torch.ops.quantized.add(
        input,
        other,
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_scale"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_zero_point"),
    )
