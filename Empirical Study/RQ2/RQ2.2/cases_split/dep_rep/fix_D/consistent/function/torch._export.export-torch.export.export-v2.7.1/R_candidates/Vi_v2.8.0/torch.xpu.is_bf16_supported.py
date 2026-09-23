def is_bf16_supported(including_emulation: bool = True) -> bool:
    r"""Return a bool indicating if the current XPU device supports dtype bfloat16."""
    if not is_available():
        return False
    return (
        including_emulation
        or torch.xpu.get_device_properties().has_bfloat16_conversions
    )
