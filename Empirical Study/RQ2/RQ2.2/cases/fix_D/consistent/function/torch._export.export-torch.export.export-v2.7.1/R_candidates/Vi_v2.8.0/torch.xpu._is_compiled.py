def _is_compiled() -> bool:
    r"""Return true if compile with XPU support."""
    return torch._C._has_xpu
