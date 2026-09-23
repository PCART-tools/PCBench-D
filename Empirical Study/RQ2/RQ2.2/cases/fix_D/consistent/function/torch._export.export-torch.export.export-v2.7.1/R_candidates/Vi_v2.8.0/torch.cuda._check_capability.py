def _check_capability():
    incompatible_gpu_warn = """
    Found GPU%d %s which is of cuda capability %d.%d.
    Minimum and Maximum cuda capability supported by this version of PyTorch is
    (%d.%d) - (%d.%d)
    """
    matched_cuda_warn = """
    Please install PyTorch with a following CUDA
    configurations: {} following instructions at
    https://pytorch.org/get-started/locally/
    """

    # Binary CUDA_ARCHES SUPPORTED by PyTorch
    CUDA_ARCHES_SUPPORTED = {
        "12.6": {"min": 50, "max": 90},
        "12.8": {"min": 70, "max": 120},
        "12.9": {"min": 70, "max": 120},
    }

    if (
        torch.version.cuda is not None and torch.cuda.get_arch_list()
    ):  # on ROCm we don't want this check
        for d in range(device_count()):
            capability = get_device_capability(d)
            major = capability[0]
            minor = capability[1]
            name = get_device_name(d)
            current_arch = major * 10 + minor
            min_arch = min(
                (_extract_arch_version(arch) for arch in torch.cuda.get_arch_list()),
                default=50,
            )
            max_arch = max(
                (_extract_arch_version(arch) for arch in torch.cuda.get_arch_list()),
                default=50,
            )
            if current_arch < min_arch or current_arch > max_arch:
                warnings.warn(
                    incompatible_gpu_warn
                    % (
                        d,
                        name,
                        major,
                        minor,
                        min_arch // 10,
                        min_arch % 10,
                        max_arch // 10,
                        max_arch % 10,
                    )
                )
                matched_arches = ""
                for arch, arch_info in CUDA_ARCHES_SUPPORTED.items():
                    if (
                        current_arch >= arch_info["min"]
                        and current_arch <= arch_info["max"]
                    ):
                        matched_arches += f" {arch}"
                if matched_arches != "":
                    warnings.warn(matched_cuda_warn.format(matched_arches))
