@register_lowering(
    prims._low_memory_max_pool2d_offsets_to_indices, type_promotion_kind=None
)
def _low_memory_max_pool2d_offsets_to_indices(
    offsets, kernel_width, input_width, stride, padding
):
    # TODO: Generalize to other max pooling flavors, and arbitrary dim

    offsets_loader = offsets.make_loader()

    def increments_to_index(h_inc, w_inc, bh, bw):
        w_in = ops.index_expr(input_width, torch.int64)
        hbase = ops.index_expr(bh * stride[0] - padding[0], torch.int64)
        wbase = ops.index_expr(bw * stride[1] - padding[1], torch.int64)
        ih = hbase + h_inc
        iw = wbase + w_inc
        return ih * w_in + iw

    def offsets_to_indices(idx):
        *prefix, bh, bw = idx
        offset = offsets_loader([*prefix, bh, bw])
        kw_const = ops.constant(kernel_width, torch.int32)
        h_inc = offset // kw_const
        w_inc = offset - (h_inc * kw_const)
        return increments_to_index(h_inc, w_inc, bh, bw)

    indices = Pointwise.create(
        device=offsets.get_device(),
        dtype=torch.int64,
        inner_fn=offsets_to_indices,
        ranges=offsets.get_size(),
    )
    return indices
