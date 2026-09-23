def _extract_arch_version(arch_string: str):
    """Extracts the architecture string from a CUDA version"""
    base = arch_string.split("_")[1]
    base = base.removesuffix("a")
    return int(base)
