def is_bf16_supported(including_emulation: bool = True):
    r"""Return a bool indicating if the current CUDA/ROCm device supports dtype bfloat16."""
    # Check for ROCm, if true return true, no ROCM_VERSION check required,
    # since it is supported on AMD GPU archs.
    if torch.version.hip:
        return True

    # If CUDA is not available, than it does not support bf16 either
    if not is_available():
        return False

    device = torch.cuda.current_device()

    # Check for CUDA version and device compute capability.
    # This is a fast way to check for it.
    cuda_version = torch.version.cuda
    if cuda_version is not None and torch.cuda.get_device_properties(device).major >= 8:
        return True

    if not including_emulation:
        return False

    # Finally try to create a bfloat16 device.
    return _check_bf16_tensor_supported(device)
