    @register_meta(torch.ops.onednn.qlinear_pointwise.binary)
    @register_meta(torch.ops.onednn.qlinear_pointwise.binary_tensor)
    def meta_qlinear_pointwise_binary(
        x,
        x_scale,
        x_zp,
        w,
        w_scale,
        w_zp,
        x_2,
        bias,
        output_scale,
        output_zero_point,
        output_dtype,
        x2_scale,
        x2_zp,
        binary_op_name,
        alpha,
        unary_op_name,
        unary_op_args,
        unary_op_algorithm,
    ):
        if binary_op_name == "sum":
            return x_2
        output_shape = list(x.shape)
        # The weight has been transposed during the qlinear weight prepack process.
        output_shape[-1] = w.shape[1]
        assert output_dtype in [torch.float32, torch.bfloat16, torch.uint8, torch.int8]
        out = x.new_empty(output_shape, dtype=output_dtype)
        return out
