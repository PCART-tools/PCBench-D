def _reference_quantized_conv2d(
    x_i8,
    x_scale,
    x_zero_point,
    x_quant_min,
    x_quant_max,
    weight_i8,
    weight_scale,
    weight_zero_point,
    weight_quant_min,
    weight_quant_max,
    bias_fp32,
    out_scale,
    out_zero_point,
    out_quant_min,
    out_quant_max,
):
    stride = [1, 1]
    padding = [0, 0]
    dilation = [1, 1]
    transposed = False
    output_padding = [0, 0]
    groups = 1
    # without using quant_min/max in clamp, the traced graph will not have quant_mi/max args.
    # This results in failure to match the pattern.
    # Therefore, we call a torch.ops.aten.clamp here
    x_i8 = torch.ops.aten.clamp(x_i8, x_quant_min, x_quant_max)
    weight_i8 = torch.ops.aten.clamp(weight_i8, weight_quant_min, weight_quant_max)

    x_i16 = x_i8.to(torch.int16)
    weight_i16 = weight_i8.to(torch.int16)
    # always set bias to None so that the same representation can work for the case
    # no matter if bias_scale == x_scale * weight_scale or not
    acc_i32 = out_dtype(
        torch.ops.aten.convolution.default,
        torch.int32,
        x_i16 - x_zero_point,
        weight_i16 - weight_zero_point,
        None,
        stride,
        padding,
        dilation,
        transposed,
        output_padding,
        groups,
    )
    # Note: we are quantizing bias with these scales without signal from user, but it might be OK
    bias_scale = x_scale * weight_scale
    # bias quantization to int32 uses bias_scale = x_scale * weight_scale due to:
    # Take linear calculation for example
    # Out_(i, j)_fp32 = Sum_(over k)[X_(i, k)_fp32 * W_(i, k)_fp32] + bias_(i)_fp32
    # Represent X, W fp32 as their dequant transforms
    # A_fp32 = (A_q - A_zero_point)/A_scale
    # Out_(i, j)_fp32 = Sum_(over k)[(X_(i, k)_fp32 - X_zp) * X_scale * (W_(i, k)_fp32 - W_zp) * W_scale] + bias_(i)_fp32
    # Factor out X_scale and W_scale
    # Out_(i, j)_fp32 = ((X_scale * W_scale) * Sum_(over k)[(X_(i, k)_fp32 - X_zp) * (W_(i, k)_fp32 - W_zp)]) + bias_(i)_fp32
    # In order to addition of bias_(i)_fp32 inside, we must do
    # Out_(i, j)_fp32 = (X_scale * W_scale) * (Sum_(over k)[(X_(i, k)_fp32 - X_zp) * (W_(i, k)_fp32 - W_zp)] + (1 / (X_scale * W_scale)) * bias_(i)_fp32)W_scale  # noqa: B950
    # Note we had to multiply bias_fp32 qith X_scale * W_scale = bias_scale
    # Thus bias quantization to int32 must be with X_scale * W_scale

    bias_i32 = out_dtype(torch.ops.aten.div.Tensor, torch.int32, bias_fp32, bias_scale)
    # Unsqueeze to match broadcast dims
    # Unfortnuately I cannot do bias_i32.unsqueeze(0) due to literal matching nightmare
    # in graph pattern replacement
    bias_i32 = bias_i32.unsqueeze(-1)
    bias_i32 = bias_i32.unsqueeze(-1)
    acc_i32 = acc_i32 + bias_i32
    # TODO: change to mul.Scalar when we make x_scale/weight_scale etc. Scalar values
    acc_i32 = (
        out_dtype(
            torch.ops.aten.mul.Tensor,
            torch.int32,
            acc_i32,
            x_scale * weight_scale / out_scale,
        )
        + out_zero_point
    )
    out_i8 = torch.ops.aten.clamp(acc_i32, out_quant_min, out_quant_max).to(torch.int8)
    return out_i8
