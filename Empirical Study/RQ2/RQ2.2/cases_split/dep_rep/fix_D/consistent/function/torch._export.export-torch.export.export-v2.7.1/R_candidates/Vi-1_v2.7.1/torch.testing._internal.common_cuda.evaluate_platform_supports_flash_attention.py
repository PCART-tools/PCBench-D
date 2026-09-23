def evaluate_platform_supports_flash_attention():
    if TEST_WITH_ROCM:
        return evaluate_gfx_arch_exact('gfx90a:sramecc+:xnack-') or evaluate_gfx_arch_exact('gfx942:sramecc+:xnack-')
    if TEST_CUDA:
        return not IS_WINDOWS and SM80OrLater
    return False
