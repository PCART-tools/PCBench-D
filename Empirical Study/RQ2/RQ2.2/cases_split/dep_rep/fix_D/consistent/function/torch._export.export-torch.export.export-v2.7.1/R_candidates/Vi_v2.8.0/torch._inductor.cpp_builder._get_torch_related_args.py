def _get_torch_related_args(
    include_pytorch: bool, aot_mode: bool
) -> tuple[list[str], list[str], list[str]]:
    from torch.utils.cpp_extension import include_paths, TORCH_LIB_PATH

    include_dirs = include_paths()
    libraries_dirs = [TORCH_LIB_PATH]
    libraries = []
    if sys.platform != "darwin" and not config.is_fbcode():
        libraries = ["torch", "torch_cpu"]
        if not aot_mode:
            libraries.append("torch_python")

    if _IS_WINDOWS:
        libraries.append("sleef")

    return include_dirs, libraries_dirs, libraries
