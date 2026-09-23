@contextlib.contextmanager
def texpr_enable_strategy(strategy):
    old = torch._C._jit_set_fusion_strategy(strategy)
    try:
        yield
    finally:
        torch._C._jit_set_fusion_strategy(old)
