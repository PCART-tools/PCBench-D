@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.quantize_per_channel),
    arg_replacement_tuples=[
        ("input", "input"),
        ("scales", "scales"),
        ("zero_points", "zero_points"),
        ("axis", "axis"),
        ("dtype", "dtype"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("scales", "scale", move_to_qparams),
        ("zero_points", "zero_point", move_to_qparams),
        ("axis", "axis", move_to_qparams),
        ("dtype", "dtype", dont_move_to_qparams),
    ],
)
@register_acc_op
def quantize_per_channel(*, input, acc_out_ty=None):
    assert acc_out_ty is not None
    qparams = TensorMetadata(*acc_out_ty).qparams
    dtype = TensorMetadata(*acc_out_ty).dtype
    return torch.quantize_per_channel(
        input,
        torch.tensor(qparams["scale"]),
        torch.tensor(qparams["zero_point"]),
        qparams["axis"],
        dtype,
    )  # type: ignore[call-overload]
