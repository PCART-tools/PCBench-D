def default_stream(device: Optional[_device_t] = None) -> Stream:
    r"""Return the default :class:`Stream` for a given device.

    Args:
        device (torch.device or int, optional): selected device. Returns
            the default :class:`Stream` for the current device, given by
            :func:`~torch.mtia.current_device`, if :attr:`device` is ``None``
            (default).
    """
    return torch._C._mtia_getDefaultStream(_get_device_index(device, optional=True))
