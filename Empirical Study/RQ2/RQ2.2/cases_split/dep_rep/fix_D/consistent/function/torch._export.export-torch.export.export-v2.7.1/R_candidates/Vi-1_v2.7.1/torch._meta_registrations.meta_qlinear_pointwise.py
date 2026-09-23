    @register_meta(torch.ops.onednn.qlinear_pointwise.default)
    @register_meta(torch.ops.onednn.qlinear_pointwise.tensor)
    def meta_qlinear_pointwise(
        x,
        x_scale,
        x_zp,
        w,
        w_scale,
        w_zp,
        bias,
        output_scale,
        output_zero_point,
        output_dtype,
        post_op_name,
        post_op_args,
        post_op_algorithm,
    ):
        output_shape = list(x.shape)
        # The weight has been transposed during the qlinear weight prepack process.
        output_shape[-1] = w.shape[1]
        assert output_dtype in [torch.float32, torch.bfloat16, torch.int8, torch.uint8]
        out = x.new_empty(output_shape, dtype=output_dtype)
        return out
