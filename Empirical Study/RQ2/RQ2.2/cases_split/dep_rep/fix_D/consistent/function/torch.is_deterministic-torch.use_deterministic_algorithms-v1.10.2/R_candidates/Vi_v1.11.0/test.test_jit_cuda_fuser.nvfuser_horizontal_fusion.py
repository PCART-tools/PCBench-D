@contextlib.contextmanager
def nvfuser_horizontal_fusion(flag):
    old_value = torch._C._jit_set_nvfuser_horizontal_mode(flag)
    try:
        yield
    finally:
        torch._C._jit_set_nvfuser_horizontal_mode(old_value)
