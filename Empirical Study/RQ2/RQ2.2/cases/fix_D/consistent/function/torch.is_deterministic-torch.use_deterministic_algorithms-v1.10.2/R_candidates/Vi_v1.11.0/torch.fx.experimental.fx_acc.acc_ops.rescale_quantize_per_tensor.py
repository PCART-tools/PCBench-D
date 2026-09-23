@register_acc_op_properties(
    AccOpProperty.pointwise, AccOpProperty.unary, AccOpProperty.quantized
)
@register_acc_op
def rescale_quantize_per_tensor(*, input, acc_out_ty=None):
    assert acc_out_ty is not None
    d = dequantize(input=input)
    return quantize_per_tensor(input=d, acc_out_ty=acc_out_ty)
