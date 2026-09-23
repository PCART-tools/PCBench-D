def definitely_channels_last_contiguous(a: Tensor) -> bool:
    return definitely_channels_last_contiguous_2d(
        a
    ) or definitely_channels_last_contiguous_3d(a)
