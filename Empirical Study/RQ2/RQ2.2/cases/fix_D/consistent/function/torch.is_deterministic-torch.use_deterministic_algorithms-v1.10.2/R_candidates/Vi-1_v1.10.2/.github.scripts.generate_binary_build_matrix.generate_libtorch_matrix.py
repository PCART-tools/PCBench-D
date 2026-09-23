def generate_libtorch_matrix(is_pr: bool) -> List[Dict[str, str]]:
    libtorch_variants = [
        "shared-with-deps",
        "shared-without-deps",
        "static-with-deps",
        "static-without-deps",
    ]
    return [
        {
            "gpu_arch_type": arch_type(arch_version),
            "gpu_arch_version": arch_version,
            "libtorch_variant": libtorch_variant,
            "devtoolset": abi_version,
            "container_image": LIBTORCH_CONTAINER_IMAGES[(arch_version, abi_version)],
        }
        # We don't currently build libtorch for rocm
        for arch_version in ["cpu"] + snip_if(is_pr, CUDA_ARCHES)
        for libtorch_variant in libtorch_variants
        # one of the values in the following list must be exactly
        # "cxx11-abi", but the precise value of the other one doesn't
        # matter
        for abi_version in ["cxx11-abi", "pre-cxx11"]
    ]
