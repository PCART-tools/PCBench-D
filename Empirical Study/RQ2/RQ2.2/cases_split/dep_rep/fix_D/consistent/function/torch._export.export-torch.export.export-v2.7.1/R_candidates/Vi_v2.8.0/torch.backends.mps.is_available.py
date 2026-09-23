@_lru_cache
def is_available() -> bool:
    r"""Return a bool indicating if MPS is currently available."""
    return torch._C._mps_is_available()
