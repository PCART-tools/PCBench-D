def _resolve_device(device_mesh: DeviceMesh) -> torch.device:
    device_type = device_mesh.device_type
    device_handle = _get_device_handle(device_type)
    assert device_handle is not None
    device_idx = device_mesh.get_rank() % device_handle.device_count()
    return torch.device(f"{device_type}:{device_idx:d}")
