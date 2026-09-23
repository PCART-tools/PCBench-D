def skipCUDAIfNoCusolver(fn):
    return skipCUDAIf(not has_cusolver(), "cuSOLVER not available")(fn)
