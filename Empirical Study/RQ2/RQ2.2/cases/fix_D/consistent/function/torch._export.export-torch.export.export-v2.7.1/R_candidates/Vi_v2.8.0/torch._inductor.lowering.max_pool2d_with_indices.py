@register_lowering(aten.max_pool2d_with_indices, type_promotion_kind=None)
def max_pool2d_with_indices(
    x,
    kernel_size,
    stride=None,
    padding=0,
    dilation=1,
    ceil_mode=False,
):
    return _max_pool_with_indices(
        x, kernel_size, stride, padding, dilation, ceil_mode, n_dim=2
    )
