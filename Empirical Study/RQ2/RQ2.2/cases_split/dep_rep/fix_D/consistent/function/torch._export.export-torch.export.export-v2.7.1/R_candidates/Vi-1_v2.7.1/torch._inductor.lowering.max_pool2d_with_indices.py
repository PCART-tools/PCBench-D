@register_lowering(aten.max_pool2d_with_indices, type_promotion_kind=None)
def max_pool2d_with_indices(
    x,
    kernel_size,
    stride=None,
    padding=0,
    dilation=1,
    ceil_mode=False,
):
    kernel_size, stride, padding, dilation, _ = max_pool2d_checks(
        x, kernel_size, stride, padding, dilation
    )

    if any(d > 1 for d in dilation):
        return fallback_max_pool2d_with_indices(
            x, kernel_size, stride, padding, dilation, ceil_mode=ceil_mode
        )

    out, offsets = _max_pool2d_with_offsets(
        x, kernel_size, stride, padding, dilation, ceil_mode
    )

    indices = _low_memory_max_pool2d_offsets_to_indices(
        offsets, kernel_size[-1], x.shape[-1], stride, padding
    )

    return out, indices
