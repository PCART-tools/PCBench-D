def _max_pool2d_with_offsets(
    x,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode=False,
):
    x.realize_hint()
    *batch, h, w = x.get_size()

    h_out, ceil_mode1 = pooling_size(h, 0, kernel_size, stride, padding, ceil_mode)
    w_out, ceil_mode2 = pooling_size(w, 1, kernel_size, stride, padding, ceil_mode)

    dtype = x.dtype
    min_value = (
        False
        if dtype is torch.bool
        else (float("-inf") if dtype.is_floating_point else torch.iinfo(dtype).min)
    )

    new_size = list(batch) + [h_out, w_out]
    if padding[0] or padding[1] or ceil_mode1 or ceil_mode2:
        x_loader = constant_boundary_condition(x, min_value, dim=2)
    else:
        x_loader = x.make_loader()

    dim = 2

    def fn_inner(idx, reduction_idx):
        prefix = idx[:-dim]
        bh = idx[-dim:]
        ih = [bh[i] * stride[i] + reduction_idx[i] - padding[i] for i in range(dim)]
        return x_loader([*prefix, *ih])

    result = Reduction.create(
        reduction_type="max",
        input_node=x,
        device=x.get_device(),
        dst_dtype=dtype,
        src_dtype=dtype,
        inner_fn=fn_inner,
        ranges=new_size,
        reduction_ranges=kernel_size,
    )
    offsets = Reduction.create(
        reduction_type="argmax",
        input_node=x,
        device=x.get_device(),
        dst_dtype=torch.int64,
        src_dtype=dtype,
        inner_fn=fn_inner,
        ranges=new_size,
        reduction_ranges=kernel_size,
    )
    if isinstance(result.data.data, Reduction):  # type: ignore[attr-defined]
        # Only realize if reduction isn't unrolled
        result.realize()
    if isinstance(offsets.data.data, Reduction):  # type: ignore[attr-defined]
        # Only realize if reduction isn't unrolled
        offsets.realize()

    return result, offsets
