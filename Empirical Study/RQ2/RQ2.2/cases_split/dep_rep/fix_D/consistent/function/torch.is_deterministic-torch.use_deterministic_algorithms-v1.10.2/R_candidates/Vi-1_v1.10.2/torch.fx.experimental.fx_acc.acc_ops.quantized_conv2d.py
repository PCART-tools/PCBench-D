@register_acc_op
def quantized_conv2d(
    *,
    input,
    weight,
    bias,
    stride,
    padding,
    dilation,
    groups,
    padding_mode,
    acc_out_ty=None,
):
    assert acc_out_ty is not None
    return torch.nn.quantized.functional.conv2d(
        input,
        weight,
        bias,
        stride,
        padding,
        dilation,
        groups,
        padding_mode,
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_scale"),
        acc_utils.get_field_from_acc_out_ty(acc_out_ty, "q_zero_point"),
    )
