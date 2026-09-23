def _fractional_pooling_offsets(samples, in_sz, out_sz, kernel_sz, dim, ndims):
    out_sz = out_sz[dim]
    in_sz = in_sz[dim]
    kernel_sz = kernel_sz[dim]
    alpha = IntTrueDiv(in_sz - kernel_sz, out_sz - 1)
    samples_loader = samples.make_loader()

    def load(prefix, i):
        sample = samples_loader([*prefix, ndims - 1 - dim])
        i_expr = ops.index_expr(i, samples.get_dtype())
        alpha_expr = ops.index_expr(alpha, samples.get_dtype())
        seq_i = ops.trunc((i_expr + sample) * alpha_expr) - ops.trunc(
            sample * alpha_expr
        )
        seq_i = ops.to_dtype(seq_i, torch.int64)

        mask = ops.lt(
            i_expr,
            ops.index_expr(out_sz - 1, torch.int64),
        )
        return ops.where(mask, seq_i, ops.index_expr(in_sz - kernel_sz, torch.int64))

    return load
