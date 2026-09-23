@contextlib.contextmanager
def tf32_on(self, tf32_precision=1e-5):
    if torch.version.hip:
        hip_allow_tf32 = os.environ.get("HIPBLASLT_ALLOW_TF32", None)
        os.environ["HIPBLASLT_ALLOW_TF32"] = "1"
    old_allow_tf32_matmul = torch.backends.cuda.matmul.allow_tf32
    old_precision = self.precision
    try:
        torch.backends.cuda.matmul.allow_tf32 = True
        self.precision = tf32_precision
        with torch.backends.cudnn.flags(enabled=None, benchmark=None, deterministic=None, allow_tf32=True):
            yield
    finally:
        if torch.version.hip:
            if hip_allow_tf32 is not None:
                os.environ["HIPBLASLT_ALLOW_TF32"] = hip_allow_tf32
            else:
                del os.environ["HIPBLASLT_ALLOW_TF32"]
        torch.backends.cuda.matmul.allow_tf32 = old_allow_tf32_matmul
        self.precision = old_precision
