@contextlib.contextmanager
def bf32_on(self, bf32_precision=1e-5):
    old_matmul_precision = torch.get_float32_matmul_precision()
    old_precision = self.precision
    try:
        torch.set_float32_matmul_precision("medium")
        self.precision = bf32_precision
        yield
    finally:
        torch.set_float32_matmul_precision(old_matmul_precision)
        self.precision = old_precision
