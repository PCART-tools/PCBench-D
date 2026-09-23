def is_available() -> bool:
    r"""Return a bool indicating if XPU is currently available."""
    # This function nerver throws.
    return device_count() > 0
