@register_acc_op_mapping(
    op_and_target=("call_function", torch.ops.quantized.batch_norm2d),
    arg_replacement_tuples=[
        ("input", "input"),
        ("weight", "weight"),
        ("bias", "bias"),
        ("running_mean", "running_mean"),
        ("running_var", "running_var"),
        ("eps", "eps"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("scale", "q_scale"),
        ("zero_point", "q_zero_point"),
    ],
)
@register_acc_op
def quantized_batch_norm2d(
    *, input, running_mean, running_var, weight, bias, eps, acc_out_ty
):
    return torch.ops.quantized.batch_norm2d(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        eps,
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_scale"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_zero_point"),
    )
