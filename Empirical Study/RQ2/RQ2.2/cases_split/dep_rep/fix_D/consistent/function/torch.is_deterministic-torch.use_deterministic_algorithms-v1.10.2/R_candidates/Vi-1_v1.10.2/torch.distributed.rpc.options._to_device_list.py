def _to_device_list(devices: List[DeviceType]) -> List[torch.device]:
    return list(map(_to_device, devices))
