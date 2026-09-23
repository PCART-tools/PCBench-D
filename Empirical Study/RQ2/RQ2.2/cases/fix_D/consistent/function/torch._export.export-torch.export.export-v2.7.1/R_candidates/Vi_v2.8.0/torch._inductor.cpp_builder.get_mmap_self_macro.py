def get_mmap_self_macro(use_mmap_weights: bool) -> list[str]:
    macros = []
    if use_mmap_weights:
        macros.append(" USE_MMAP_SELF")
    return macros
