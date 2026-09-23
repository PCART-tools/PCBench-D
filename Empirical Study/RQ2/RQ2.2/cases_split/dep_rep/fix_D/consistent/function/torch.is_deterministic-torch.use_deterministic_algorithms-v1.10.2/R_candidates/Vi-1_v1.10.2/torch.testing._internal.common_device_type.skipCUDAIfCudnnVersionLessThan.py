def skipCUDAIfCudnnVersionLessThan(version=0):

    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if self.device_type == 'cuda':
                if self.no_cudnn:
                    reason = "cuDNN not available"
                    raise unittest.SkipTest(reason)
                if self.cudnn_version is None or self.cudnn_version < version:
                    reason = "cuDNN version {0} is available but {1} required".format(self.cudnn_version, version)
                    raise unittest.SkipTest(reason)

            return fn(self, *args, **kwargs)

        return wrap_fn
    return dec_fn
