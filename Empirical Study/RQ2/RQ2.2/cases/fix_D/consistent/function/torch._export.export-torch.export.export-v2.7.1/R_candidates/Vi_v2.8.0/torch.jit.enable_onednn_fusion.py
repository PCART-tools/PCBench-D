def enable_onednn_fusion(enabled: bool):
    """Enable or disables onednn JIT fusion based on the parameter `enabled`."""
    torch._C._jit_set_llga_enabled(enabled)
