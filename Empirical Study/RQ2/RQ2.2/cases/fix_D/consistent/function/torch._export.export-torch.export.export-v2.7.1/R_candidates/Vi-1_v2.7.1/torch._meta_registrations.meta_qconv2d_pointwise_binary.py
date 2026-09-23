    @register_meta(torch.ops.onednn.qconv2d_pointwise.binary)
    def meta_qconv2d_pointwise_binary(
        x,
        x_scale,
        x_zp,
        w,
        w_scale,
        w_zp,
        accum,
        bias,
        stride,
        padding,
        dilation,
        groups,
        output_scale,
        output_zero_point,
        output_dtype,
        accum_scale,
        accum_zero_point,
        binary_op_name,
        alpha,
        unary_op_name,
        unary_op_args,
        unary_op_algorithm,
    ):
        assert binary_op_name == "sum"
        return accum
