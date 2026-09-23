@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op_properties(AccOpProperty.quantized)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.quantize_per_tensor),
    arg_replacement_tuples=[
        ("input", "input"),
        ("scale", "scale"),
        ("zero_point", "zero_point"),
        ("dtype", "dtype"),
    ],
    kwargs_to_move_to_acc_out_ty=[
        ("scale", "scale", move_to_qparams),
        ("zero_point", "zero_point", move_to_qparams),
        ("dtype", "dtype", dont_move_to_qparams),
    ],
)
@register_acc_op
def quantize_per_tensor(*, input, acc_out_ty=None):
    assert acc_out_ty is not None
    qparams = TensorMetadata(*acc_out_ty).qparams
    dtype = TensorMetadata(*acc_out_ty).dtype
    return torch.quantize_per_tensor(
        input, qparams["scale"], qparams["zero_point"], dtype
    )
