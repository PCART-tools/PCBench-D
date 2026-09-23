def _register_quantization_unary_lowering():
    # QConv2d
    for users in [1, 2]:
        qconv_pattern = get_qconv2d_pt2e_pattern(users)
        _register_quantized_conv_lowering(
            qconv_pattern,
            2,  # pass_number
            torch.ops.onednn.qconv2d_pointwise.default,  # computation_op
        )

    # QLinear
    for x_scale_zp_are_tensors in (False, True):
        qlinear_pattern = get_qlinear_pt2e_pattern(x_scale_zp_are_tensors)
        computation_op = (
            torch.ops.onednn.qlinear_pointwise.tensor
            if x_scale_zp_are_tensors
            else torch.ops.onednn.qlinear_pointwise.default
        )
        _register_quantized_linear_unary_lowering(
            qlinear_pattern,
            2,  # pass_number
            computation_op,
        )
