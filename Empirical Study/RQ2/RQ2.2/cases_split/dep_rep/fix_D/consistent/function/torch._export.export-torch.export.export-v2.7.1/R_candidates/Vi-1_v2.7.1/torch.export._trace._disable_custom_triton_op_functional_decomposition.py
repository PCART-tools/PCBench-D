@contextmanager
def _disable_custom_triton_op_functional_decomposition():
    old = torch._functorch.config.decompose_custom_triton_ops
    try:
        torch._functorch.config.decompose_custom_triton_ops = False
        yield torch._functorch.config.decompose_custom_triton_ops
    finally:
        torch._functorch.config.decompose_custom_triton_ops = old
