def is_available():
    r"""Return whether PyTorch is built with NNPACK support."""
    return torch._nnpack_available()
