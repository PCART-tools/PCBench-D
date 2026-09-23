def _fractional_pooling_offsets(samples, in_sz, out_sz, kernel_sz, dim, ndims):
    out_sz = out_sz[dim]
    in_sz = in_sz[dim]
    kernel_sz = kernel_sz[dim]
    samples_loader = samples.make_loader()

    def load(prefix, i):
        sample = samples_loader([*prefix, ndims - 1 - dim])
        i_expr = ops.index_expr(i, samples.get_dtype())
        diff = ops.index_expr(in_sz - kernel_sz, torch.int64)
        out_sz_expr = ops.index_expr(out_sz - 1, torch.int64)
        alpha = ops.truediv(
            ops.to_dtype(diff, torch.float64), ops.to_dtype(out_sz_expr, torch.float64)
        )
        alpha = ops.where(ops.eq(out_sz_expr, 0), 0, alpha)
        seq_i = ops.trunc((i_expr + sample) * alpha) - ops.trunc(sample * alpha)
        seq_i = ops.to_dtype(seq_i, torch.int64)
        mask = ops.lt(i_expr, out_sz_expr)
        return ops.indirect_indexing(ops.where(mask, seq_i, diff), sympy.sympify(in_sz))

    return load
