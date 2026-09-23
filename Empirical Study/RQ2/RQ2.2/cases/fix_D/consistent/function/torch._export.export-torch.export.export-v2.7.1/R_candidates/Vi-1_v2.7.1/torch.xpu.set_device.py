def set_device(device: _device_t) -> None:
    r"""Set the current device.

    Args:
        device (torch.device or int or str): selected device. This function is a
            no-op if this argument is negative.
    """
    _lazy_init()
    device = _get_device_index(device)
    if device >= 0:
        torch._C._xpu_setDevice(device)
