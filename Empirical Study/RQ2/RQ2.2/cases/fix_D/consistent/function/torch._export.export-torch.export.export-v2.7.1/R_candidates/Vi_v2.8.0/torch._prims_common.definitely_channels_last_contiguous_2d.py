def definitely_channels_last_contiguous_2d(a: Tensor) -> bool:
    return is_channels_last_contiguous_2d(a, false_if_dde=True)
