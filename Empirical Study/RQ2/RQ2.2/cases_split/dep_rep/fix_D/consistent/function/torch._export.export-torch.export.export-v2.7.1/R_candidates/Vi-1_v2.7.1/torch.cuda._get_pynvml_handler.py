def _get_pynvml_handler(device: Optional[Union[Device, int]] = None):
    if not _HAS_PYNVML:
        raise ModuleNotFoundError(
            "pynvml does not seem to be installed or it can't be imported."
        ) from _PYNVML_ERR
    from pynvml import NVMLError_DriverNotLoaded

    try:
        pynvml.nvmlInit()
    except NVMLError_DriverNotLoaded as e:
        raise RuntimeError("cuda driver can't be loaded, is cuda enabled?") from e

    device = _get_nvml_device_index(device)
    handle = pynvml.nvmlDeviceGetHandleByIndex(device)
    return handle
