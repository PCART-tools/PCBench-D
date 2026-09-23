def current_stream(device: torch.device) -> AbstractStream:
    """:func:`torch.cuda.current_stream` for either CPU or CUDA device."""
    if device.type != "cuda":
        return CPUStream
    return torch.cuda.current_stream(device)
