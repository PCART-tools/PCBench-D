def _to_will_alias(
    a: TensorLikeType,
    device: Optional[DeviceLikeType] = None,
    dtype: Optional[torch.dtype] = None,
    copy: Optional[bool] = None,
    layout: Optional[torch.layout] = None,
    memory_format: Optional[torch.memory_format] = None,
    pin_memory: Optional[bool] = False,
    non_blocking: bool = False,  # not using non_blocking
) -> bool:
    return (
        not copy
        and (device is None or a.device == device)
        and (dtype is None or a.dtype == dtype)
        and (layout is None or a.layout == layout)
        # is_pinned issue #84925
        # and (pin_memory is None or pin_memory == a.is_pinned())
        and (
            memory_format is None
            or memory_format == torch.preserve_format
            or utils.is_contiguous_for_memory_format(a, memory_format=memory_format)
        )
    )
