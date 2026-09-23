def current_device() -> int:
    r"""Return the index of a currently selected device."""
    return torch._C._accelerator_hooks_get_current_device()
