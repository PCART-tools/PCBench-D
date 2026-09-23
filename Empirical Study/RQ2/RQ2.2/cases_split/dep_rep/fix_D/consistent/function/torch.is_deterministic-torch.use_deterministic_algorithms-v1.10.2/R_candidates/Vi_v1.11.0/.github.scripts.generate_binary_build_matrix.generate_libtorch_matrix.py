def generate_libtorch_matrix(os: str, abi_version: str) -> List[Dict[str, str]]:
    libtorch_variants = [
        "shared-with-deps",
        "shared-without-deps",
        "static-with-deps",
        "static-without-deps",
    ]
    ret: List[Dict[str, str]] = []
    arches = ["cpu"]
    if os == "linux":
        arches += CUDA_ARCHES
    elif os == "windows":
        # We don't build CUDA 10.2 for window see https://github.com/pytorch/pytorch/issues/65648
        arches += list_without(CUDA_ARCHES, ["10.2"])
    for arch_version in arches:
        for libtorch_variant in libtorch_variants:
            # We don't currently build libtorch for rocm
            # one of the values in the following list must be exactly
            # CXX11_ABI, but the precise value of the other one doesn't
            # matter
            gpu_arch_type = arch_type(arch_version)
            gpu_arch_version = "" if arch_version == "cpu" else arch_version
            ret.append(
                {
                    "gpu_arch_type": gpu_arch_type,
                    "gpu_arch_version": gpu_arch_version,
                    "desired_cuda": translate_desired_cuda(
                        gpu_arch_type, gpu_arch_version
                    ),
                    "libtorch_variant": libtorch_variant,
                    "libtorch_config": abi_version if os == "windows" else "",
                    "devtoolset": abi_version if os != "windows" else "",
                    "container_image": LIBTORCH_CONTAINER_IMAGES[
                        (arch_version, abi_version)
                    ] if os != "windows" else "",
                    "package_type": "libtorch",
                    "build_name": f"libtorch-{gpu_arch_type}{gpu_arch_version}-{libtorch_variant}-{abi_version}".replace(
                        ".", "_"
                    ),
                }
            )
    return ret
