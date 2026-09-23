def generate_wheels_matrix(is_pr: bool) -> List[Dict[str, str]]:
    arches = ["cpu"]
    arches += snip_if(is_pr, CUDA_ARCHES)
    arches += snip_if(is_pr, ROCM_ARCHES)
    return [
        {
            "python_version": python_version,
            "gpu_arch_type": arch_type(arch_version),
            "gpu_arch_version": arch_version,
            "container_image": WHEEL_CONTAINER_IMAGES[arch_version],
        }
        for python_version in snip_if(is_pr, FULL_PYTHON_VERSIONS)
        for arch_version in arches
    ]
