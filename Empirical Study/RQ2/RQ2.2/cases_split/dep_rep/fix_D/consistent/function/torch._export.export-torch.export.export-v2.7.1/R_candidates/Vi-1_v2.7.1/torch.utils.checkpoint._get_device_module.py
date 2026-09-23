def _get_device_module(device="cuda"):
    if device == "meta":
        return torch.device("meta")
    device_module = getattr(torch, device)
    return device_module
