def get_processor_arch_name(gpu_version):
    return "cpu" if not gpu_version else (
        "cu" + gpu_version.strip("cuda") if gpu_version.startswith("cuda") else gpu_version
    )
