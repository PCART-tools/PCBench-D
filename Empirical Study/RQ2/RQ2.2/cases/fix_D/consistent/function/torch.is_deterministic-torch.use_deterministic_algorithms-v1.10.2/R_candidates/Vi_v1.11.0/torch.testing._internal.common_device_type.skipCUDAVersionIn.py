def skipCUDAVersionIn(versions : List[Tuple[int, int]] = None):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            version = _get_torch_cuda_version()
            if version == (0, 0):  # cpu
                return fn(self, *args, **kwargs)
            if version in (versions or []):
                reason = "test skipped for CUDA version {0}".format(version)
                raise unittest.SkipTest(reason)
            return fn(self, *args, **kwargs)

        return wrap_fn
    return dec_fn
