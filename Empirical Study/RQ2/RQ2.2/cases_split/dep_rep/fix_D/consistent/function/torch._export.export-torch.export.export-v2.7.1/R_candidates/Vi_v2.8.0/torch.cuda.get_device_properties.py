def get_device_properties(device: "Device" = None) -> _CudaDeviceProperties:
    r"""Get the properties of a device.

    Args:
        device (torch.device or int or str, optional): device for which to return the
            properties of the device.  It uses the current device, given by
            :func:`~torch.cuda.current_device`, if :attr:`device` is ``None``
            (default).

    Returns:
        _CudaDeviceProperties: the properties of the device
    """
    _lazy_init()  # will define _get_device_properties
    device = _get_device_index(device, optional=True)
    if device < 0 or device >= device_count():
        raise AssertionError("Invalid device id")
    return _get_device_properties(device)  # type: ignore[name-defined]
