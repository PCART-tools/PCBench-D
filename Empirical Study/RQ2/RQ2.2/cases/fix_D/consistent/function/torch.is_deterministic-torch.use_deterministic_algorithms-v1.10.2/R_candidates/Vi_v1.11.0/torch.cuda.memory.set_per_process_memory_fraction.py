def set_per_process_memory_fraction(fraction, device: Union[Device, int] = None) -> None:
    r"""Set memory fraction for a process.
    The fraction is used to limit an caching allocator to allocated memory on a CUDA device.
    The allowed value equals the total visible memory multiplied fraction.
    If trying to allocate more than the allowed value in a process, will raise an out of
    memory error in allocator.

    Args:
        fraction(float): Range: 0~1. Allowed memory equals total_memory * fraction.
        device (torch.device or int, optional): selected device. If it is
            ``None`` the default CUDA device is used.
    .. note::
        In general, the total available free memory is less than the total capacity.
    """
    _lazy_init()
    if device is None:
        device = torch.cuda.current_device()
    device = _get_device_index(device)
    if not isinstance(fraction, float):
        raise TypeError('Invalid type for fraction argument, must be `float`')
    if fraction < 0 or fraction > 1:
        raise ValueError('Invalid fraction value: {}. '
                         'Allowed range: 0~1'.format(fraction))

    torch._C._cuda_setMemoryFraction(fraction, device)
