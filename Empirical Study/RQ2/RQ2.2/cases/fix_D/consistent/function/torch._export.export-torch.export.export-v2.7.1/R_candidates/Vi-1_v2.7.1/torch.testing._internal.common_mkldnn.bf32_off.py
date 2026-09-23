@contextlib.contextmanager
def bf32_off():
    old_matmul_precision = torch.get_float32_matmul_precision()
    try:
        torch.set_float32_matmul_precision("highest")
        yield
    finally:
        torch.set_float32_matmul_precision(old_matmul_precision)
