def get_device_op_overrides(device: str) -> DeviceOpOverrides:
    assert isinstance(device, str), type(device)

    if not device_op_overrides_dict:
        from . import cpu_device_op_overrides, mps_device_op_overrides  # noqa: F401
        from .cuda import device_op_overrides  # noqa: F401
        from .xpu import device_op_overrides as xpu_op_overrides  # noqa: F401

    return device_op_overrides_dict[device]
