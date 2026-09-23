def get_default_device() -> "torch.device":
    r"""Gets the default ``torch.Tensor`` to be allocated on ``device``"""
    global _GLOBAL_DEVICE_CONTEXT

    from torch.overrides import _get_current_function_mode_stack
    from torch.utils._device import DeviceContext

    def _get_device_with_index(device):
        if device.index is not None:
            return device
        else:
            # TODO: Call like get_device_index() method corresponding to
            # each device type
            return torch.tensor([]).device

    # Get device from any active DeviceContext.
    device_mode = next(
        filter(
            lambda mode: isinstance(mode, DeviceContext),
            reversed(_get_current_function_mode_stack()),
        ),
        None,
    )
    if device_mode:
        device = device_mode.device
        return _get_device_with_index(device)

    if hasattr(_GLOBAL_DEVICE_CONTEXT, "device_context"):
        device = _GLOBAL_DEVICE_CONTEXT.device_context.device
        return _get_device_with_index(device)
    else:
        return torch.device("cpu")
