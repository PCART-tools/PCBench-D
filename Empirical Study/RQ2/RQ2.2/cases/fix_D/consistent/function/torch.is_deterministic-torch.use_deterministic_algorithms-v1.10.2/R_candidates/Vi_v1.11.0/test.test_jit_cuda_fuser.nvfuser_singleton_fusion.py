@contextlib.contextmanager
def nvfuser_singleton_fusion(flag):
    old_value = torch._C._jit_set_nvfuser_single_node_mode(flag)
    try:
        yield
    finally:
        torch._C._jit_set_nvfuser_single_node_mode(old_value)
