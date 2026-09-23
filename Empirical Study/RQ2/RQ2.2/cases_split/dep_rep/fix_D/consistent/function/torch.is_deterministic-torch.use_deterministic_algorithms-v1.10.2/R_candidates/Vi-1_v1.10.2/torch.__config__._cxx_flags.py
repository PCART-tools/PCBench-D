def _cxx_flags():
    """Returns the CXX_FLAGS used when building PyTorch."""
    return torch._C._cxx_flags()
