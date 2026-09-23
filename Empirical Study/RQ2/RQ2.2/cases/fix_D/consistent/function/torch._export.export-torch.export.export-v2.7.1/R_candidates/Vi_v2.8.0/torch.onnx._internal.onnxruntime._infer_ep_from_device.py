def _infer_ep_from_device(*args) -> tuple[str, ...]:
    """Return the first valid device (i.e., GPU or CPU) in argument list."""
    eps = []
    for arg in args:
        if hasattr(arg, "device"):
            device = arg.device
            if device.type == "cuda":
                eps.append("CUDAExecutionProvider")
            elif device.type == "cpu":
                eps.append("CPUExecutionProvider")
    return tuple(eps)
