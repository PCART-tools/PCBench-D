def can_device_access_peer(device: _device_t, peer_device: _device_t) -> bool:
    r"""Check if peer access between two devices is possible."""
    _lazy_init()
    device = _get_device_index(device, optional=True)
    peer_device = _get_device_index(peer_device)
    if device < 0 or device >= device_count():
        raise AssertionError("Invalid device id")
    if peer_device < 0 or peer_device >= device_count():
        raise AssertionError("Invalid peer device id")
    return torch._C._cuda_canDeviceAccessPeer(device, peer_device)
