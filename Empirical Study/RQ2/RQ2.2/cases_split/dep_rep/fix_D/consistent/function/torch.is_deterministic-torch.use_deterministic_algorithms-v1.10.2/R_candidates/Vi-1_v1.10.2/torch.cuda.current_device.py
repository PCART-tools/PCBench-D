def current_device() -> int:
    r"""Returns the index of a currently selected device."""
    _lazy_init()
    return torch._C._cuda_getDevice()
