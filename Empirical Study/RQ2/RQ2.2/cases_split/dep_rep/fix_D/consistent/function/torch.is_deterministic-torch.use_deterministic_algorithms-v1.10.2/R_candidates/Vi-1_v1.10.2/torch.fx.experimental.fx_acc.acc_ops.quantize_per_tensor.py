@register_acc_op_mapping(
    op_and_target=("call_function", torch.quantize_per_tensor),
    arg_replacement_tuples=[
        ("input", "input"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
        ("dtype", "dtype"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("dtype", "dtype"),
        ("scale", "q_scale"),
        ("zero_point", "q_zero_point"),
    ],
)
@register_acc_op
def quantize_per_tensor(*, input, acc_out_ty=None):
    assert acc_out_ty is not None
    return torch.quantize_per_tensor(
        input,
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_scale"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_zero_point"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "dtype"),
    )
