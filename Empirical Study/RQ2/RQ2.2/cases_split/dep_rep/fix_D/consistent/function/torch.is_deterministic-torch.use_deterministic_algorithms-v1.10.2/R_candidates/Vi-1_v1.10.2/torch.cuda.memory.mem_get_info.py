def mem_get_info(device: Union[Device, int] = None) -> int:
    r"""Returns the global free and total GPU memory occupied for a given
    device using cudaMemGetInfo.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    .. note::
        See :ref:`cuda-memory-management` for more
        details about GPU memory management.
    """
    if device is None:
        device = torch.cuda.current_device()
    device = _get_device_index(device)
    return torch.cuda.cudart().cudaMemGetInfo(device)
