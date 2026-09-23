def get_device_capability(device: Optional[_device_t] = None) -> tuple[int, int]:
    r"""Return capability of a given device as a tuple of (major version, minor version).

    Args:
        device (torch.device or int, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).
    """
    return torch._C._mtia_getDeviceCapability(_get_device_index(device, optional=True))
