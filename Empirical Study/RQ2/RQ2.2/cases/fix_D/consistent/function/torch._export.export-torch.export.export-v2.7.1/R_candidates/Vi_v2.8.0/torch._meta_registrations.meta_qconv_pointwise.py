    @register_meta(torch.ops.onednn.qconv2d_pointwise.default)
    @register_meta(torch.ops.onednn.qconv_pointwise.default)
    def meta_qconv_pointwise(
        x,
        x_scale,
        x_zp,
        w,  # prepacked_weight
        w_scale,
        w_zp,
        bias,
        stride,
        padding,
        dilation,
        groups,
        output_scale,
        output_zero_point,
        output_dtype,
        attr,
        scalars,
        algorithm,
    ):
        shape_out = calc_conv_nd_return_shape(
            x,
            w,
            stride,
            padding,
            dilation,
            False,
            groups,
            None,
        )
        assert output_dtype in [torch.float32, torch.bfloat16, torch.uint8, torch.int8]
        out = x.new_empty(shape_out, dtype=output_dtype)
        assert len(shape_out) in [3, 4], "only conv1d/2d are supported"
        format = torch.channels_last if len(shape_out) == 4 else torch.contiguous_format
        out = out.to(memory_format=format)
        return out
