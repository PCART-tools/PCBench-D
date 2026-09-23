@register_lowering(aten.fractional_max_pool2d)
def fractional_max_pool2d(x, kernel_size, output_size, random_samples):
    x.realize_hint()
    *batch, inp_h, inp_w = x.get_size()
    kernel_h, kernel_w = kernel_size
    h_out, w_out = output_size

    if kernel_h * kernel_w >= 25:
        return fallback_fractional_max_pool2d(
            x, kernel_size, output_size, random_samples
        )

    gen_offsets_for_dim = functools.partial(
        _fractional_pooling_offsets,
        samples=random_samples,
        in_sz=[inp_h, inp_w],
        out_sz=output_size,
        kernel_sz=kernel_size,
        ndims=2,
    )

    h_index_fn = gen_offsets_for_dim(dim=0)
    w_index_fn = gen_offsets_for_dim(dim=1)
    x_loader = x.make_loader()

    def fn(idx, return_index):
        *prefix, bh, bw = idx

        h_start_index = ops.indirect_indexing(h_index_fn(prefix, bh), inp_h)
        w_start_index = ops.indirect_indexing(w_index_fn(prefix, bw), inp_w)

        maxval = None
        maxindex = None
        for ih, iw in itertools.product(range(kernel_size[0]), range(kernel_size[1])):
            val = x_loader([*prefix, h_start_index + ih, w_start_index + iw])
            if return_index:
                index = ops.index_expr(
                    (h_start_index + ih) * inp_w + w_start_index + iw, torch.int64
                )
                if maxindex is None:
                    maxindex = index
                else:
                    maxindex = ops.where(
                        ops.or_(ops.gt(val, maxval), ops.isnan(val)), index, maxindex
                    )
            if maxval is None:
                maxval = val
            else:
                maxval = ops.maximum(val, maxval)
        if return_index:
            return maxindex
        else:
            return maxval

    new_size = list(batch) + [h_out, w_out]
    rv = Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=functools.partial(fn, return_index=False),
        ranges=new_size,
    )

    ri = Pointwise.create(
        device=x.get_device(),
        dtype=torch.int64,
        inner_fn=functools.partial(fn, return_index=True),
        ranges=new_size,
    )
    return rv, ri
