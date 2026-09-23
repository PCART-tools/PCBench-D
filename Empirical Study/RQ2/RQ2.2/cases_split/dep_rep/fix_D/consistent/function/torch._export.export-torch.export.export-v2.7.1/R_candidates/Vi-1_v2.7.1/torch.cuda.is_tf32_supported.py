def is_tf32_supported() -> bool:
    r"""Return a bool indicating if the current CUDA/ROCm device supports dtype tf32."""
    # Check for ROCm.  If true, return false, since PyTorch does not currently support
    # tf32 on ROCm.
    if torch.version.hip:
        return False

    # Otherwise, tf32 is supported on CUDA platforms that natively (i.e. no emulation)
    # support bfloat16.
    return is_bf16_supported(including_emulation=False)
