@register_acc_op_properties(AccOpProperty.quantized)
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
        ("scale", "scale", move_to_qparams),
        ("zero_point", "zero_point", move_to_qparams),
    ],
)
@register_acc_op
def quantized_batch_norm2d(
    *, input, running_mean, running_var, weight, bias, eps, acc_out_ty
):
    qparams = TensorMetadata(*acc_out_ty).qparams
    return torch.ops.quantized.batch_norm2d(
        input,
        weight,
        bias,
        running_mean,
        running_var,
        eps,
        qparams["scale"],
        qparams["zero_point"],
    )
