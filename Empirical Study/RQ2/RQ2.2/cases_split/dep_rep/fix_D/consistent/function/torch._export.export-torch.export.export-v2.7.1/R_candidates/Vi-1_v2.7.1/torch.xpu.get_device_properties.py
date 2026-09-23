def get_device_properties(device: Optional[_device_t] = None) -> _XpuDeviceProperties:
    r"""Get the properties of a device.

    Args:
        device (torch.device or int or str): device for which to return the
            properties of the device.

    Returns:
        _XpuDeviceProperties: the properties of the device
    """
    _lazy_init()
    device = _get_device_index(device, optional=True)
    return _get_device_properties(device)  # type: ignore[name-defined]  # noqa: F821
