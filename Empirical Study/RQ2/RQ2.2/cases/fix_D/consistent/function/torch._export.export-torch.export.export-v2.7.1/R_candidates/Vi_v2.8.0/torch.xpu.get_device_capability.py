@lru_cache(None)
def get_device_capability(device: Optional[_device_t] = None) -> dict[str, Any]:
    r"""Get the xpu capability of a device.

    Args:
        device (torch.device or int or str, optional): device for which to
            return the device capability. This function is a no-op if this
            argument is a negative integer. It uses the current device, given by
            :func:`~torch.xpu.current_device`, if :attr:`device` is ``None``
            (default).

    Returns:
        Dict[str, Any]: the xpu capability dictionary of the device
    """
    props = get_device_properties(device)
    # pybind service attributes are no longer needed and their presence breaks
    # the further logic related to the serialization of the created dictionary.
    # In particular it filters out `<bound method PyCapsule._pybind11_conduit_v1_ of _XpuDeviceProperties..>`
    # to fix Triton tests.
    # This field appears after updating pybind to 2.13.6.
    return {
        prop: getattr(props, prop)
        for prop in dir(props)
        if not prop.startswith(("__", "_pybind11_"))
    }
