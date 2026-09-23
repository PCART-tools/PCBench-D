    @register_meta(torch.ops.onednn.linear_dynamic_fp16.default)
    @register_meta(torch.ops.onednn.linear_relu_dynamic_fp16.default)
    def meta_linear_dynamic_fp16(
        x,
        w,
        bias,
    ):
        output_shape = list(x.shape)
        # The weight has been transposed during the qlinear weight prepack process.
        output_shape[-1] = w.shape[1]
        out = x.new_empty(output_shape)
        return out
