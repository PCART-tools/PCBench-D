def _is_compiled() -> bool:
    r"""Return true if compiled with MTIA support."""
    return torch._C._mtia_isBuilt()
