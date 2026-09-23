@contextmanager
def _disable_jit_autocast():
    old_jit_autocast_flag = torch._C._jit_set_autocast_mode(False)
    try:
        yield
    finally:
        torch._C._jit_set_autocast_mode(old_jit_autocast_flag)
