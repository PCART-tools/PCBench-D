def needs_fallback_due_to_atomic_add_limitations(dtype: torch.dtype) -> bool:
    # tl.atomic add has bfloat16 support in fbcode
    # but not in OSS https://github.com/pytorch/pytorch/issues/97016
    # we will fallback until the code is upstreamed to OSS
    if (
        config.is_fbcode()
        and dtype == torch.bfloat16
        and torch.cuda.is_available()
        and torch.cuda.get_device_capability() >= (9, 0)
        and config.bfloat16_atomic_adds_enabled
    ):
        return False
    else:
        return dtype in OrderedSet([torch.int64, torch.bool, torch.bfloat16])
