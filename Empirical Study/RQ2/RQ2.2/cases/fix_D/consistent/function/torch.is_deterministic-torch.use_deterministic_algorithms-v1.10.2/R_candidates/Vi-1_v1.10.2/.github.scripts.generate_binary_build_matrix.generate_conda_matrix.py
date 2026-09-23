def generate_conda_matrix(is_pr: bool) -> List[Dict[str, str]]:
    return [
        {
            "python_version": python_version,
            "gpu_arch_type": arch_type(arch_version),
            "gpu_arch_version": arch_version,
            "container_image": CONDA_CONTAINER_IMAGES[arch_version],
        }
        for python_version in snip_if(is_pr, FULL_PYTHON_VERSIONS)
        # We don't currently build conda packages for rocm
        for arch_version in ["cpu"] + snip_if(is_pr, CUDA_ARCHES)
    ]
