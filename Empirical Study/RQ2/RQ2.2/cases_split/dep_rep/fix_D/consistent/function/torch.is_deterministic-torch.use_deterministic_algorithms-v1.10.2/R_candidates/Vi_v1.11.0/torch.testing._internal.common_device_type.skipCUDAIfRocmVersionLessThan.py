def skipCUDAIfRocmVersionLessThan(version=None):

    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if self.device_type == 'cuda':
                if not TEST_WITH_ROCM:
                    reason = "ROCm not available"
                    raise unittest.SkipTest(reason)
                rocm_version = str(torch.version.hip)
                rocm_version = rocm_version.split("-")[0]    # ignore git sha
                rocm_version_tuple = tuple(int(x) for x in rocm_version.split("."))
                if rocm_version_tuple is None or version is None or rocm_version_tuple < tuple(version):
                    reason = "ROCm {0} is available but {1} required".format(rocm_version_tuple, version)
                    raise unittest.SkipTest(reason)

            return fn(self, *args, **kwargs)

        return wrap_fn
    return dec_fn
