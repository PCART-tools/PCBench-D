def _is_avx512_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AVX512."""
    return torch._C._cpu._is_avx512_supported()
