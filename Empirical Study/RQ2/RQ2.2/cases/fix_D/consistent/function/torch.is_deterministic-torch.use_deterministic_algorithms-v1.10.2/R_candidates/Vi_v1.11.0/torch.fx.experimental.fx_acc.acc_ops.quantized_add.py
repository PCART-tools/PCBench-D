@register_acc_op_properties(AccOpProperty.quantized)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.ops.quantized.add),
    arg_replacement_tuples=[
        ("qa", "input"),
        ("qb", "other"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("scale", "scale", move_to_qparams),
        ("zero_point", "zero_point", move_to_qparams),
    ],
)
@register_acc_op
def quantized_add(*, input, other, acc_out_ty=None):
    assert acc_out_ty is not None
    qparams = TensorMetadata(*acc_out_ty).qparams
    return torch.ops.quantized.add(
        input,
        other,
        qparams["scale"],
        qparams["zero_point"],
    )
