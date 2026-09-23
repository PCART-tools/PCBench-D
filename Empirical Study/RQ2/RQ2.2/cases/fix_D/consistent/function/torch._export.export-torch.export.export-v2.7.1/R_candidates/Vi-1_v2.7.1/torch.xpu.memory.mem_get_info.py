def mem_get_info(device: _device_t = None) -> tuple[int, int]:
    r"""Return the global free and total GPU memory for a given device.

    Args:
        device (torch.device or int or str, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.xpu.current_device`,
            if :attr:`device` is ``None`` (default).

    Returns:
        int: the memory available on the device in units of bytes.
        int: the total memory on the device in units of bytes
    """
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_getMemoryInfo(device)
