def use_persistent_tma(k: sympy.core.numbers.Integer, has_bias: bool) -> bool:
    available = has_triton_tma_device() and triton_config.enable_persistent_tma_matmul
    # _determine_swizzle_mode_2d requires BLOCK_K to be at least 32 contiguous bytes
    # When K is 16, BLOCK_K = 16 and is not valid
    min_k = k >= 32
    return available and min_k and not has_bias
