def _get_stream(device: int):
    """Gets a background stream for copying between CPU and GPU"""
    global _streams
    if device == -1:
        return None
    if _streams is None:
        _streams = [None] * torch.cuda.device_count()
    if _streams[device] is None:
        _streams[device] = torch.cuda.Stream(device)
    return _streams[device]
