def _get_device_from_device_id(
    device_id: Optional[Union[int, torch.device]],
    rank: int,
    device_handle: _FSDPDeviceHandle,
) -> Optional[torch.device]:
    """
    Return a ``torch.device`` for the specified ``device_id``.

    Processes ``device_id`` and returns either the corresponding device or
    ``None`` if ``device_id`` is ``None``.
    """
    if device_id is None:
        return None
    device = (
        device_id if isinstance(device_id, torch.device) else torch.device(device_id)
    )
    if device.type != "cpu" and device.index is None:
        warnings.warn(
            f"FSDP got the argument `device_id` {device_id} on rank "
            f"{rank}, which does not have an explicit index. "
            f"FSDP will use the current device {device_handle.current_device()}. "
            f"If this is incorrect, please explicitly call `torch.{device.type}.set_device()` "
            "before FSDP initialization or pass in the explicit device "
            "index as the `device_id` argument."
        )
        device = torch.device(device_handle.current_device())
    return device
