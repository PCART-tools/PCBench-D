def is_available() -> bool:
    r"""Returns a bool indicating if CUDA is currently available."""
    if not hasattr(torch._C, '_cuda_getDeviceCount'):
        return False
    # This function never throws and returns 0 if driver is missing or can't
    # be initialized
    return torch._C._cuda_getDeviceCount() > 0
