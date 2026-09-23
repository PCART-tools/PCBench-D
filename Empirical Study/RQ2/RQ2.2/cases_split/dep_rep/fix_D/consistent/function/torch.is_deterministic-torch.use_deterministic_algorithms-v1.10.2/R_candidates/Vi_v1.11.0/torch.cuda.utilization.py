def utilization(device: Optional[Union[Device, int]] = None) -> int:
    r"""Returns the percent of time over the past sample period during which one or
    more kernels was executing on the GPU as given by `nvidia-smi`.

    Args:
        device (torch.device or int, optional): selected device. Returns
            statistic for the current device, given by :func:`~torch.cuda.current_device`,
            if :attr:`device` is ``None`` (default).

    Warning: Each sample period may be between 1 second and 1/6 second,
    depending on the product being queried.
    """
    try:
        import pynvml  # type: ignore[import]
    except ModuleNotFoundError:
        raise ModuleNotFoundError("pynvml module not found, please install pynvml")
    from pynvml import NVMLError_DriverNotLoaded
    try:
        pynvml.nvmlInit()
    except NVMLError_DriverNotLoaded:
        raise RuntimeError("cuda driver can't be loaded, is cuda enabled?")
    device = _get_device_index(device, optional=True)
    handle = pynvml.nvmlDeviceGetHandleByIndex(device)
    return pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
