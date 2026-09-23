def canonicalize_device(device: DeviceLikeType) -> torch.device:
    if isinstance(device, torch.device):
        return device

    assert isinstance(device, str)
    return torch.device(device)
