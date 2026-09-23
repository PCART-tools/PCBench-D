def get_default_device() -> "torch.device":
    r"""Gets the default ``torch.Tensor`` to be allocated on ``device``"""
    global _GLOBAL_DEVICE_CONTEXT

    if hasattr(_GLOBAL_DEVICE_CONTEXT, "device_context"):
        device = _GLOBAL_DEVICE_CONTEXT.device_context.device
        if device.index is not None:
            return device
        else:
            # TODO: Call like get_device_index() method corresponding to
            # each device type
            return torch.tensor([]).device
    else:
        return torch.device("cpu")
