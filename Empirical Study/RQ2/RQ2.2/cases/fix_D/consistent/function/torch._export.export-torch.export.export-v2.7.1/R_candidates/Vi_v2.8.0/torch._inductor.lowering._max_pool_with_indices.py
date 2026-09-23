def _max_pool_with_indices(
    x,
    kernel_size,
    stride,
    padding,
    dilation,
    ceil_mode,
    n_dim,
):
    kernel_size, stride, padding, dilation, _ = max_pool_checks(
        x, kernel_size, stride, padding, dilation, n_dim=n_dim
    )

    out, offsets = _max_pool_with_offsets(
        x, kernel_size, stride, padding, dilation, ceil_mode, n_dim=n_dim
    )

    indices = _low_memory_max_pool_offsets_to_indices(
        offsets,
        kernel_size,
        x.shape[-n_dim:],
        stride,
        padding,
        dilation,
    )

    return out, indices
