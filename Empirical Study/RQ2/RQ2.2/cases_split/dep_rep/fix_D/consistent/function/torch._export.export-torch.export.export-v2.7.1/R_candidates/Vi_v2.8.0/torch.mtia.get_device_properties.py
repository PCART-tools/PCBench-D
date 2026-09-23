def get_device_properties(device: Optional[_device_t] = None) -> dict[str, Any]:
    r"""Return a dictionary of MTIA device properties

    Args:
        device (torch.device or int, optional) selected device. Returns
            statistics for the current device, given by current_device(),
            if device is None (default).
    """
    return torch._C._mtia_getDeviceProperties(_get_device_index(device, optional=True))
