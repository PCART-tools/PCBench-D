def is_available():
    r"""Return whether PyTorch is built with MKL support."""
    return torch._C.has_mkl
