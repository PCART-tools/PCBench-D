def skipCUDAIfNoMagmaAndNoCusolver(fn):
    version = _get_torch_cuda_version()
    if version >= (10, 2):
        return fn
    else:
        # cuSolver is disabled on cuda < 10.1.243, tests depend on MAGMA
        return skipCUDAIfNoMagma(fn)
