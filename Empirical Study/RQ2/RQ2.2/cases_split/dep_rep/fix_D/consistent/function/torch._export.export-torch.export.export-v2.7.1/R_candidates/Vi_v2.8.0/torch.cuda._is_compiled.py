def _is_compiled() -> bool:
    r"""Return true if compile with CUDA support."""
    return hasattr(torch._C, "_cuda_getDeviceCount")
