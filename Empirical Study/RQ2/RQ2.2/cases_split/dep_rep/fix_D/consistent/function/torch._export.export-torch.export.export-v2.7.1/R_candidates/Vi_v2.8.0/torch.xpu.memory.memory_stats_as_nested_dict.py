def memory_stats_as_nested_dict(device: _device_t = None) -> dict[str, Any]:
    r"""Return the result of :func:`~torch.xpu.memory_stats` as a nested dictionary."""
    if not is_initialized():
        return {}
    device = _get_device_index(device, optional=True)
    return torch._C._xpu_memoryStats(device)
