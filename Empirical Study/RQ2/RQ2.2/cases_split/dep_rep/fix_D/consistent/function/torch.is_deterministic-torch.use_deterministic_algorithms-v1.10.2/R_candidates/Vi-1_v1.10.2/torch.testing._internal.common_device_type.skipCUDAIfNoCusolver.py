def skipCUDAIfNoCusolver(fn):
    version = _get_torch_cuda_version()
    return skipCUDAIf(version < (10, 2), "cuSOLVER not available")(fn)
