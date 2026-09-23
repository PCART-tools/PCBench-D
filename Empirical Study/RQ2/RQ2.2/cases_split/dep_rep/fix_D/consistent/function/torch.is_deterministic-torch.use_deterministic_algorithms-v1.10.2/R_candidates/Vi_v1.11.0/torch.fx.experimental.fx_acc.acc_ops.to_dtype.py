@register_acc_op_properties(AccOpProperty.pointwise, AccOpProperty.unary)
@register_acc_op
def to_dtype(input, acc_out_ty=None):
    assert acc_out_ty is not None
    return input.to(dtype=TensorMetadata(*acc_out_ty).dtype)
