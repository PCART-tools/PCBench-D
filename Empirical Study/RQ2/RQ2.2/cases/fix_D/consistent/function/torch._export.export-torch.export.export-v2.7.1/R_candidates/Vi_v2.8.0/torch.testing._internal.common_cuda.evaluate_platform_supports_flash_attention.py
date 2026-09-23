def evaluate_platform_supports_flash_attention():
    if TEST_WITH_ROCM:
        arch_list = ["gfx90a", "gfx942", "gfx1100", "gfx1201", "gfx950"]
        if os.environ.get("TORCH_ROCM_AOTRITON_ENABLE_EXPERIMENTAL", "0") != "0":
            arch_list += ["gfx1101", "gfx1150", "gfx1151", "gfx1200"]
        return evaluate_gfx_arch_within(arch_list)
    if TEST_CUDA:
        return not IS_WINDOWS and SM80OrLater
    return False
