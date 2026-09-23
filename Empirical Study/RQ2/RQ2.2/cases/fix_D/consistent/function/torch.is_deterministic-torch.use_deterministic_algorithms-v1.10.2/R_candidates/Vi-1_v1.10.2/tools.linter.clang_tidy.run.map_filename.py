def map_filename(build_folder: str, fname: str) -> str:
    fname = os.path.relpath(fname)
    native_cpu_prefix = "aten/src/ATen/native/cpu/"
    build_cpu_prefix = os.path.join(build_folder, native_cpu_prefix, "")
    default_arch_suffix = ".DEFAULT.cpp"
    if fname.startswith(native_cpu_prefix) and fname.endswith(".cpp"):
        return (
            f"{build_cpu_prefix}{fname[len(native_cpu_prefix):]}{default_arch_suffix}"
        )
    if fname.startswith(build_cpu_prefix) and fname.endswith(default_arch_suffix):
        return f"{native_cpu_prefix}{fname[len(build_cpu_prefix):-len(default_arch_suffix)]}"
    return fname
