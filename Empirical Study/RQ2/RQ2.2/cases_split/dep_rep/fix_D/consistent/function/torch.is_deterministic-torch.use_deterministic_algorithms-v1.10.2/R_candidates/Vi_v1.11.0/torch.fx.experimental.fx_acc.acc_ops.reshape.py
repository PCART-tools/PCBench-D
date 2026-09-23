@register_acc_op_properties(AccOpProperty.unary)
@register_acc_op_mapping(
    op_and_target=("call_function", torch.reshape),
    arg_replacement_tuples=[
        ("input", "input"),
        ("shape", "shape"),
    ],
    kwargs_to_move_to_acc_out_ty=[("shape", "shape")],
)
@register_acc_op_mapping(
    op_and_target=("call_method", "view"),
    arg_replacement_tuples=[
        ("input", "input"),
        ("*", "shape"),
    ],
    kwargs_to_move_to_acc_out_ty=[("shape", "shape")],
)
@register_acc_op
def reshape(*, input, acc_out_ty=None):
    assert acc_out_ty is not None
    return input.reshape(TensorMetadata(*acc_out_ty).shape)
