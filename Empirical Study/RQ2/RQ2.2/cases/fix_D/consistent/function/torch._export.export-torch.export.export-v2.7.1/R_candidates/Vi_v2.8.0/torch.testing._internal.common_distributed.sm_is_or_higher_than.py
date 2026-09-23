def sm_is_or_higher_than(device: torch.device, major: int, minor: int) -> bool:
    """
    Returns True if the device's compute capability is (major, minor) or higher.
    Error out if the device is not a CUDA device.
    Returns False if device is a RoCM device.
    """
    if device.type != "cuda":
        raise ValueError("sm_is_or_later() is only supported for CUDA devices")

    if torch.version.hip is not None:
        # ROCm devices may have different compute capability codes
        return False

    return torch.cuda.get_device_capability(device) >= (major, minor)
