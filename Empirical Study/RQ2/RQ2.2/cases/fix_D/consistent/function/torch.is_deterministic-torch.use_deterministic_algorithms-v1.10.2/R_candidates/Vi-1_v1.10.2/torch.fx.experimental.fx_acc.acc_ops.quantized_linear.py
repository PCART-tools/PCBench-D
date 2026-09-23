@register_acc_op
def quantized_linear(*, input, weight, bias, acc_out_ty=None):
    assert acc_out_ty is not None
    return nn.quantized.functional.linear(
        input,
        weight,
        bias,
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_scale"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_zero_point"),
    )
