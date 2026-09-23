def onednn_fusion_enabled():
    """Return whether onednn JIT fusion is enabled."""
    return torch._C._jit_llga_enabled()
