    @register_meta(torch.ops.mkldnn._convolution_pointwise.default)
    def meta_mkldnn_convolution_default(
        input_tensor,
        weight,
        bias,
        padding,
        stride,
        dilation,
        groups,
        attr,
        scalars,
        algorithm,
    ):
        shape_out = calc_conv_nd_return_shape(
            input_tensor, weight, stride, padding, dilation, False, groups, []
        )
        out = input_tensor.new_empty(shape_out)
        out_memory_format = torch.channels_last
        if input_tensor.dim() == 5:
            out_memory_format = torch.channels_last_3d
        out = out.to(memory_format=out_memory_format)  # type: ignore[call-overload]
        return out
