def require_backends_available(backends):
    def check(backend):
        if backend == dist.Backend.GLOO:
            return dist.is_gloo_available()
        if backend == dist.Backend.NCCL:
            return dist.is_nccl_available()
        if backend == dist.Backend.MPI:
            return dist.is_mpi_available()
        return False

    if not all(check(dist.Backend(backend)) for backend in backends):
        return sandcastle_skip("Test requires backends to be available %s" % backends)
    return lambda func: func
