def get_gencode_flags() -> str:
    r"""Return XPU AOT(ahead-of-time) build flags this library was compiled with."""
    arch_list = get_arch_list()
    if len(arch_list) == 0:
        return ""
    return f'-device {",".join(arch for arch in arch_list)}'
