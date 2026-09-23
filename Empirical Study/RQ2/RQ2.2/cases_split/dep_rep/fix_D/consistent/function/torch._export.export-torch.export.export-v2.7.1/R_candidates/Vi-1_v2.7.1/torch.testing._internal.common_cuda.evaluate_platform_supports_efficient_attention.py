def evaluate_platform_supports_efficient_attention():
    if TEST_WITH_ROCM:
        return evaluate_gfx_arch_exact('gfx90a:sramecc+:xnack-') or evaluate_gfx_arch_exact('gfx942:sramecc+:xnack-')
    if TEST_CUDA:
        return True
    return False
