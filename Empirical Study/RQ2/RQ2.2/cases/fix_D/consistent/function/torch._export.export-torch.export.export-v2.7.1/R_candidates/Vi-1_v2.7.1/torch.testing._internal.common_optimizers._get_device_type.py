def _get_device_type(device: Union[str, torch.device]) -> str:
    # Returns the device type as a string, e.g., "cpu" or "cuda"
    if isinstance(device, torch.device):
        device = str(device.type)
    assert isinstance(device, str)
    return device.split(":")[0]
