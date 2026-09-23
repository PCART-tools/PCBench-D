def get_per_process_memory_fraction(device: "Device" = None) -> float:
    r"""Get memory fraction for a process.

    Args:
        device (torch.device or int, optional): selected device. If it is
            ``None`` the default CUDA device is used.
    Returns:
        memory fraction, in range 0~1. Allowed memory equals total_memory * fraction.
    """
    _lazy_init()
    if device is None:
        device = torch.cuda.current_device()
    device = _get_device_index(device)
    return torch._C._cuda_getMemoryFraction(device)
