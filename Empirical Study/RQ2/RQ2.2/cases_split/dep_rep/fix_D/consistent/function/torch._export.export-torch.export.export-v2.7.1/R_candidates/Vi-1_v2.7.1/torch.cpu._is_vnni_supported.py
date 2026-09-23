def _is_vnni_supported() -> bool:
    r"""Returns a bool indicating if CPU supports VNNI."""
    # Note: Currently, it only checks avx512_vnni, will add the support of avx2_vnni later.
    return torch._C._cpu._is_avx512_vnni_supported()
