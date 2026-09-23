def _check_capability():
    incorrect_binary_warn = """
    Found GPU%d %s which requires CUDA_VERSION >= %d to
     work properly, but your PyTorch was compiled
     with CUDA_VERSION %d. Please install the correct PyTorch binary
     using instructions from https://pytorch.org
    """  # noqa: F841

    old_gpu_warn = """
    Found GPU%d %s which is of cuda capability %d.%d.
    PyTorch no longer supports this GPU because it is too old.
    The minimum cuda capability supported by this library is %d.%d.
    """

    if torch.version.cuda is not None:  # on ROCm we don't want this check
        CUDA_VERSION = torch._C._cuda_getCompiledVersion()  # noqa: F841
        for d in range(device_count()):
            capability = get_device_capability(d)
            major = capability[0]
            minor = capability[1]
            name = get_device_name(d)
            current_arch = major * 10 + minor
            min_arch = min(
                (_extract_arch_version(arch) for arch in torch.cuda.get_arch_list()),
                default=35,
            )
            if current_arch < min_arch:
                warnings.warn(
                    old_gpu_warn
                    % (d, name, major, minor, min_arch // 10, min_arch % 10)
                )
