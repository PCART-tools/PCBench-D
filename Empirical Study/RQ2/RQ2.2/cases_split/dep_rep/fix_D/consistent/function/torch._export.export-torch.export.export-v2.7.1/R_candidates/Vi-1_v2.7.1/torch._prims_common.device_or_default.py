def device_or_default(device: Optional[DeviceLikeType]) -> DeviceLikeType:
    return device if device is not None else torch.device("cpu")
