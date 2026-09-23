@functools.cache
def split_aot_inductor_output_path(path: str) -> tuple[str, str]:
    """Returns the path where the AOT Inductor compiled kernels are stored."""
    if path.endswith(".so"):
        return os.path.split(path)
    elif path.endswith(".pt2"):
        return os.path.split(path)
    else:
        return path, ""
