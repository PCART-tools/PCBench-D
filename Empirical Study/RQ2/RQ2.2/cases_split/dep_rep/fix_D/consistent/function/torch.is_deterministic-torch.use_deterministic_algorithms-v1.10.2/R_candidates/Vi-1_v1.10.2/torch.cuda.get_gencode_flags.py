def get_gencode_flags() -> str:
    r"""Returns NVCC gencode flags this library was compiled with."""
    arch_list = get_arch_list()
    if len(arch_list) == 0:
        return ""
    arch_list_ = [arch.split("_") for arch in arch_list]
    return " ".join([f"-gencode compute=compute_{arch},code={kind}_{arch}" for (kind, arch) in arch_list_])
