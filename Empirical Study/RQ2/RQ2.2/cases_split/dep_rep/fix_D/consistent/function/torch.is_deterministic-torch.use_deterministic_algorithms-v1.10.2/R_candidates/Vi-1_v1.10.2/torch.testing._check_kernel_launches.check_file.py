def check_file(filename):
    """Checks a file for CUDA kernel launches without cuda error checks

    Args:
        filename - File to check

    Returns:
        The number of unsafe kernel launches in the file
    """
    if not (filename.endswith(".cu") or filename.endswith(".cuh")):
        return 0
    if should_exclude_file(filename):
        return 0
    fo = open(filename, "r")
    contents = fo.read()
    unsafeCount = check_code_for_cuda_kernel_launches(contents, filename)
    fo.close()
    return unsafeCount
