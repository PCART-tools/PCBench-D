def generate_wheels_matrix(os: str) -> List[Dict[str, str]]:
    arches = ["cpu"]
    package_type = "wheel"
    if os == "linux":
        arches += CUDA_ARCHES + ROCM_ARCHES
        # NOTE: We only build manywheel packages for linux
        package_type = "manywheel"
    elif os == "windows":
        # We don't build CUDA 10.2 for window see https://github.com/pytorch/pytorch/issues/65648
        arches += list_without(CUDA_ARCHES, ["10.2"])
    ret: List[Dict[str, str]] = []
    for python_version in FULL_PYTHON_VERSIONS:
        for arch_version in arches:
            gpu_arch_type = arch_type(arch_version)
            gpu_arch_version = "" if arch_version == "cpu" else arch_version
            ret.append(
                {
                    "python_version": python_version,
                    "gpu_arch_type": gpu_arch_type,
                    "gpu_arch_version": gpu_arch_version,
                    "desired_cuda": translate_desired_cuda(
                        gpu_arch_type, gpu_arch_version
                    ),
                    "container_image": WHEEL_CONTAINER_IMAGES[arch_version],
                    "package_type": package_type,
                    "build_name": f"{package_type}-py{python_version}-{gpu_arch_type}{gpu_arch_version}".replace(
                        ".", "_"
                    ),
                }
            )
    return ret
