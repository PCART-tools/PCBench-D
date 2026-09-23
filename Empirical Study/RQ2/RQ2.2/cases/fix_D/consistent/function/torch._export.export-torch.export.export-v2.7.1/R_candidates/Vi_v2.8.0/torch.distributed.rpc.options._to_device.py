def _to_device(device: DeviceType) -> torch.device:
    device = torch.device(device)
    if device.type != "cuda":
        raise ValueError(
            "`set_devices` expect a list of CUDA devices, but got "
            f"device type {device.type}."
        )
    return device
