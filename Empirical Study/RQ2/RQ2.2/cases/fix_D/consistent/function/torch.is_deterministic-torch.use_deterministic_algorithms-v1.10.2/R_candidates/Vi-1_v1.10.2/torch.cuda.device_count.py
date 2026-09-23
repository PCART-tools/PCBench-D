def device_count() -> int:
    r"""Returns the number of GPUs available."""
    if is_available():
        return torch._C._cuda_getDeviceCount()
    else:
        return 0
