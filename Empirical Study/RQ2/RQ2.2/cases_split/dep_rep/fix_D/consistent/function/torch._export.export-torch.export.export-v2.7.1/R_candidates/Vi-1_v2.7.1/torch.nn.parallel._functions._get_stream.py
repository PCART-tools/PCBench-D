def _get_stream(device: torch.device):
    """Get a background stream for copying between CPU and target device."""
    global _streams
    if device.type == "cpu":
        return None
    device_mod = getattr(torch, device.type, None)
    if device_mod is None:
        return None
    if _streams is None:
        _streams = [None] * device_mod.device_count()
    if _streams[device.index] is None:
        _streams[device.index] = device_mod.Stream(device.index)
    return _streams[device.index]
