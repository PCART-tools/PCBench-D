def use_aten_gemm_kernels() -> bool:
    return not use_max_autotune() or _use_autotune_backend("ATEN")
