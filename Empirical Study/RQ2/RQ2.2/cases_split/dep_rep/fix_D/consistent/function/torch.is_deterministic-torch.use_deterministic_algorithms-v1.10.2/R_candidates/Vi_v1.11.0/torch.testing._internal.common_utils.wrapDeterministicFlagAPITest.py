def wrapDeterministicFlagAPITest(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with DeterministicGuard(
                torch.are_deterministic_algorithms_enabled(),
                warn_only=torch.is_deterministic_algorithms_warn_only_enabled()):
            class CuBLASConfigGuard:
                cublas_var_name = 'CUBLAS_WORKSPACE_CONFIG'

                def __enter__(self):
                    self.is_cuda10_2_or_higher = (
                        (torch.version.cuda is not None)
                        and ([int(x) for x in torch.version.cuda.split(".")] >= [10, 2]))
                    if self.is_cuda10_2_or_higher:
                        self.cublas_config_restore = os.environ.get(self.cublas_var_name)
                        os.environ[self.cublas_var_name] = ':4096:8'

                def __exit__(self, exception_type, exception_value, traceback):
                    if self.is_cuda10_2_or_higher:
                        cur_cublas_config = os.environ.get(self.cublas_var_name)
                        if self.cublas_config_restore is None:
                            if cur_cublas_config is not None:
                                del os.environ[self.cublas_var_name]
                        else:
                            os.environ[self.cublas_var_name] = self.cublas_config_restore
            with CuBLASConfigGuard():
                fn(*args, **kwargs)
    return wrapper
