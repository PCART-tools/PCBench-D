@functools.cache
def nvcc_exist(nvcc_path: Optional[str] = "nvcc") -> bool:
    return nvcc_path is not None and shutil.which(nvcc_path) is not None
