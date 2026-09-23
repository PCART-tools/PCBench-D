@register_acc_op_properties(AccOpProperty.quantized)
@register_acc_op
def quantized_linear(*, input, weight, bias, acc_out_ty=None):
    assert acc_out_ty is not None
    qparams = TensorMetadata(*acc_out_ty).qparams
    return nn.quantized.functional.linear(
        input,
        weight,
        bias,
        qparams["scale"],
        qparams["zero_point"],
    )
