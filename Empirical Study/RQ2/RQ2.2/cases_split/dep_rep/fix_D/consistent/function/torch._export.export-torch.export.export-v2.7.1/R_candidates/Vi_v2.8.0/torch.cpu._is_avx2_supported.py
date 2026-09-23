def _is_avx2_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AVX2."""
    return torch._C._cpu._is_avx2_supported()
